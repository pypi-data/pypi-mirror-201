"""
# "Parameter System"

A scheme to "automatically" dispatch methods to derive values for requested
parameters. This scheme is similar to the overloading scheme of
`func_utils.overload` but distinct in some critical ways. While `overload`
resembles method overloading from object oriented programming, this rule system
resembles more a constraint satisfaction system as in prolog.

We demonstrate the parameter system via examples below. 

## The Basics

Parameters are subclasses of `type_utils.Parameter`. They can be treated as
types.

```python
    PArg1 = Parameter("first argument", doc="some documentation about it", typ=int)
    PArg2 = Parameter(...)
    PArg3 = Parameter(...)
```

Then lets say we want to define a function `fun` that accepts some parameters
which we want to be derived automatically:

```python
    def fun(arg1: PArg1, arg2: PArg2) -> int:
        return arg1 + arg2
```

The main interface to the parameter inference system is the `Rules` class,
instantiated and instrumented as follows:

```python
    rules = Rules()
    
    @rules.register_rules
    class Inferences:
        def name_does_not_matter() -> PArg1:
            return 42

        def infer_arg2(arg3: PArg3) -> PArg2:
            return arg3 + 100

        def infer_arg3(arg1: PArg1) -> PArg3:
            return arg1
```

This indicates that the class `Inferences` contains inference rules to be used
for deriving values for parameters. The names of the functions is not important.
Their type annotations are used for determining which rules are applicable to a
derivation. `infer_arg2`, for example, is a "rule" that can infer a value for
`PArg2` if it is provided a value for `PArg3`.

In order to call `fun` which needs both `PArg1` and `PArg2` we can use
`Rules.bind`:

```python
    binding = rules.bind(func=fun, ...)
    # Hidden parameters are for a case when you have some part of `fun`'s args. 
    # Ignore the fact that `bind` returns iterable, more on that later.
```

This gives you BoundArgumets which you can use to call `fun`:

```python
    result = fun(*binding.args, **binding.kwargs)
```

Under the hood, `Rules.bind` derives values for `fun`'s arguments using the
rules registered earlier. In the process it calls all of the registered methods.
Notice that it needs to use `infer_arg3` indirectly to be able to call
`infer_arg2`.

## Rule Arguments

The first notable difference between overloading and the rules system is that
the arguments to the rules are selected (and derived) only as needed for the
implementations of those rules. That is, even if we have derived a value for
something prior to deriving a parameter does not mean it will be included in all
subsequent calls. For example, `infer_arg3` above requires only `PArg1` so this
rule will be called only with a value for that argument, and not others like
`PArg2` which was a requirement of `fun` which initiated the derivation process
to begin with.

## Multiple Outputs and their Consistency

The second major difference between this scheme and overloading is that rules
support returning more than one parameter at once and enforcement of consistency
between returned parameters. By consistency here we mean that if a rule is used
that returns more than 1 parameter, those parameters should keep the values they
attained simultanously due to that one rule, and no other rule is allowed to
override one of those parameters. Thus the multiple parameters remain consistent
with each other, being produced together.

To use this feature, define rules with outputs annotated as tuples of
parameters:

```python
    def multiout_rule(...) -> (PArg1, PArg2):
        return (100, 42)
```

Note that even you need to derive just `PArg1` and do not care about `PArg2`, it
is still appropriate to use this rule.

## Multiple Derivations

The rule system is meant to better handle the possibility of multiple
different derivations producing potentially different assignments to the
parameters. In the above example, we actually need to use `bind` like this:

```python
    for binding in rules.bind(func=fun, ...):
        result = fun(*binding.args, **binding.kwargs)
```

That is, `rules.bind` returns an iterable of possible bindings, each derived
differently. While it does not check that the resulting `BoundArguments` are
actually different, this is an expected possibility.

## Names and Parameter Matching

The system derives values for parameters based on the annotations for registered
rules. The way in which an appropriate rules are determined has some subtleties.
First, to derive a value for `PArg1`, any rule that has `PArg1` specifically in
its tuple of outputs can be used. However, a value for this argument can also be
derived via rules for other parameters and if another parameter (matching as
described below) is already known, it can be used for `PArg1`.

A value for parameter `PArg2` can be used as a value for `PArg1` if these
parameters have the same name AND the type of PArg2 is a subtype of PArg1. Save
for the name requirement, this is identical to typical subtyping usage in object
oriented programming: a type B can be used where A is expected whenever B is a
subtype of A.

The subtyping is similar to how `overload` operates but the name requirement
introduces some flexibility and some rigidity. First, the names of the rule
arguments do not matter, only the parameter in their annotations. That is, in
the examples above, names `arg1`, `arg2`, `arg3` are irrelevant. This means it
is easy to get multiple values for parameters that have similar function. For
example, in NLP ingestion, one can define:

```python

    PTorchModel = Parameter("model", doc="a pytorch model", typ=torch.nn.Module)
    PHugsModel = Parameter("model", doc="a huggingface model", typ=...)

    def set_model1(model: PHugsModel): ...
        # use a hugs model

    def set_model2(
        name_does_not_matter: PTorchModel, name_irrelevant: PHugsModel
    ): ...
        # use both a torch model and a huggingface model derived from it, they 
        # may even be the same
```

On the other hand, there is some additional rigidity. In `set_model2`, a value
provided for `name_does_not_matter` is a pytorch model which could also be a
huggingface model (huggingface models are subclasses of torch models). A rule
that expects a huggingface model will not be able to take in the value we passed
in as `name_does_not_matter`, even if it is a huggingface model because the
annotation was a pytorch model. One can write rules, however, to do this
conversion:

```python
    def downcast_torch_model(model: PModelTorch) -> PModelHugsTextClassifier:
        if isinstance(model, PModelHugsTextClassifier):
            return model
```

TODO: Decide whether it is ok to use a huggingface model here even if its
annotated with pytorch model even though this goes against intuitions from
object oriented programming.
"""

from __future__ import annotations

import collections
from dataclasses import dataclass
import inspect
from inspect import Parameter as IParameter
from inspect import signature
from itertools import chain
import logging
import os
from typing import Any, Callable, DefaultDict, Dict, Iterable, List
from typing import Optional as TOptional
from typing import Tuple

from truera.client.util.debug import render_exception
from truera.client.util.debug import retab
from truera.client.util.func import sig_eval_annotations
from truera.client.util.python_utils import Annotation
from truera.client.util.python_utils import caller_globals
from truera.client.util.type_utils import fullname
from truera.client.util.types import Function
from truera.client.util.types import Given
from truera.client.util.types import Optional
from truera.client.util.types import Parameter

logger = logging.getLogger(name=__name__)

StateDict = Dict[Parameter, Any]

# Follow up work to move this to a set of things that will be available to write from the tutorial
# JIRA#MLNN-463
INGESTION_CUSTOM_KEYS = set(
    [
        'model',
        'get_model',  # autowrap
        'eval_model',  # autowrap
        'vocab',  # autowrap
        'unk_token_id',  # autowrap
        'pad_token_id',  # autowrap
        'special_tokens',  # autowrap
        'text_to_inputs',  # autowrap
        'text_to_token_ids',  # autowrap
        'text_to_spans',  # autowrap
        'n_embeddings',  # autowrap
        'n_tokens',  # autowrap
        'ds_from_source',  # autowrap
        'standardize_databatch',  # autowrap
        'embedding_layer',  # NLPAttributionConfiguration
        'embedding_anchor',  # NLPAttributionConfiguration
        'output_layer',  # NLPAttributionConfiguration
        'output_anchor',  # NLPAttributionConfiguration
        'n_output_neurons',  # NLPAttributionConfiguration
        'n_metrics_records',  # NLPAttributionConfiguration
        'ref_token',  # NLPAttributionConfiguration
        'resolution',  # NLPAttributionConfiguration
        'rebatch_size',  # NLPAttributionConfiguration
    ]
)

# TODO(piotrm): tracing of rule derivation
#
# How traces should look like. After calling set_model(pytorch_model=something, pad_token=None):
#   Trace for pytorch_model:
#     via "Input"
#   Trace for parameter pad_token:
#     via "Rule tokens_of_huggingface_tokenizer"
#     via "Rule huggingface_tokenizer of huggingface_model"
#     via "Rule huggingface_model of pytorch_model"
#   Trace for parameter mask_token:
#     "Alongside pad_token" (if mask_token is not an arg to set_model)
#     ... rest is the same as pad_token


@dataclass
class Tracepoint(object):
    """
    Class for noting various points in the derivation of an inferrable parameter.
    """

    pass


@dataclass
class ViaRule(Tracepoint):
    """
    The use of a rule.
    """

    rule: Rule


@dataclass
class ViaStronger(Tracepoint):
    """
    The use of a parameter that is stronger than the one asked for. For example,
    PModelTorch is "stronger" than PModel. If a rule or dispatch option calls
    for PModel, it is appropriate to give it PModelTorch instead as PModelTorch
    is a subclass of PModel.
    """

    stronger: Parameter


@dataclass
class ViaInput(Tracepoint):
    """
    The use of an explicit method input, that is, not an inference.
    """
    pass


class State(collections.abc.Iterable):
    """
    A state assigns a value to parameters. Also includes a "trace" for each
    value indicating how it was derived.
    """

    def __init__(self, values: StateDict):
        self.values: StateDict = {}
        self.trace: DefaultDict[
            Parameter, List[Tracepoint]] = collections.defaultdict(list)

        for k, v in values.items():
            self.set(k, v)

    def bind_relevant_and_call(self, func):
        """
        Call the given func with values coming from self. Does not do any
        inference as values are already assumed to be present.
        """

        sig = signature(func)

        kwargs = dict()

        for name, param in sig.parameters.items():
            if isinstance(param.annotation, Parameter):
                assert param.annotation in self.values, f"state does not have a value for parameter {name}: {param.annotation}"
                kwargs[name] = self.get(param.annotation)
            elif isinstance(param.annotation, Given
                           ) and isinstance(param.annotation.typ, Parameter):
                assert param.annotation.typ in self.values, f"state does not have a value for given parameter {name}: {param.annotation}"
                kwargs[name] = self.get(param.annotation.typ)
            else:
                values = [v for k, v in self.values.items() if k.name == name]
                assert len(
                    values
                ) <= 1, f"had none or more than 1 possible binding for non-parameter input named {name}"

                if len(values) == 1:
                    kwargs[name] = values[0]
                else:
                    assert param.default is not IParameter.empty, f"state has no value for non-default argument named {name}"

        binding = sig.bind(**kwargs)

        return func(*binding.args, **binding.kwargs)

    def update(self, state: 'State'):
        """
        Update self with the parameters/traces in the given `state`.
        """

        for k, v in state.values.items():
            self.set(k, v, trace=state.trace[k])

        return self

    def delete(self, var: 'Parameter') -> None:
        assert var in self.values, f"Parameter {var} not in state to delete."

        self.values.__delitem__(var)

    def set(
        self,
        var: 'Parameter',
        val: Any,
        trace: TOptional[List[Tracepoint]] = None
    ):
        """
        Set the value `val` for the given parameter `val`. Set its trace to `trace`.
        """

        trace = trace or []

        if var in self:
            if self.get(var) != val:
                raise Backtrack(
                    f"attempting to override parameter {var}={self.get(var)} with value {val} ."
                )

        self.values[var] = val
        self.trace[var] = trace

    def get(self, var: 'Parameter') -> Any:
        """
        Get the value of the given parameter `var`.
        """
        return self.values.get(var)

    def __iter__(self):
        return iter(self.values)

    @staticmethod
    def is_stronger(a: Parameter, b: Parameter) -> bool:
        """
        Determine whether `a` is "stronger" than `b` in that `a` can be used in
        places where `b` is expected. This is just a subclass check along with a
        name comparison. Not using the LogicalType system for name comparison,
        could not figure out how to do that.
        """

        return a.name == b.name and issubclass(a, b)

    def get_stronger(self: 'State', var: Parameter) -> Iterable[Any]:
        """
        Get variables that imply the given parameter `var`, other than `var`
        itself.
        """

        for stronger in self:
            if var == stronger:  # skip `var` itself if it is in state.
                continue

            if State.is_stronger(stronger, var):
                yield stronger

    @staticmethod
    def _val_summary(val: Any, max_len: int = 32) -> str:
        str_val = str(val)

        if "\n" in str_val:
            lines = str_val.split("\n")

            str_val = lines[0]
            while str_val == "" and len(lines) > 1:
                lines = lines[1:]
                str_val = lines[0]

            if len(lines) > 1:
                str_val += "..."

        if len(str_val) > max_len:
            str_val = str_val[0:max_len - 2] + "..."

        return str_val

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        ret = "\n"
        for var, val in self.values.items():
            str_val = self._val_summary(val, max_len=64)

            typename = fullname(type(val))

            if (not typename.startswith("builtins")
               ) or ("function" in typename):
                if hasattr(val, "__name__") and val.__name__ is not None:
                    str_val += f"\n\t\t__name__ = {self._val_summary(val.__name__, max_len=64)}"
                if hasattr(val, "__doc__") and val.__doc__ is not None:
                    str_val += f"\n\t\t__doc__ = {self._val_summary(val.__doc__, max_len=64)}"

            ret += f"\t{var}: {self._val_summary(typename, max_len=32)} = {str_val}\n"  # via {self.trace[var]}\n"
        return ret

    # TODO: method might not be used any more
    def is_valid(self, var: 'Parameter') -> bool:
        """
        Determine whether that given parameter `var` is satisfied by this state,
        this is if it is explicitly set or is otherwise implied by something
        that is.
        """

        if var in self:
            return True

        if any(State.is_stronger(stronger, var) for stronger in self):
            return True

        return False

    def copy(self):
        return State({}).update(self)


class Rule:
    """
    An inference rule derived from a python function that takes in variable
    assignment (state) of some subset of variables (from method signature) that
    satisfy the rule's antecedent and produces an assignment for some other
    variables (from signature's return) that satisfy the rule's consequent.

    Python functions for defining these rules can only have VarStatement
    annotations on inputs and outputs, or optionally no or non-Statement
    annotations which are interpreted as VarNotNone with or without VarTyped.
    """

    imp: Callable  # "imp" for "implementation"
    sig: inspect.Signature
    sig_annot: inspect.Signature

    name: str  # rule name
    doc: str

    consequents: Tuple[Parameter]
    antecedents: Tuple[Parameter]

    consequents_annot: Tuple[Annotation]
    antecedents_annot: Tuple[Annotation]

    def __str__(self):
        return f"{self.name}"  # :{self.antecedents} -> {self.consequents}"

    __repr__ = __str__

    def __init__(
        self,
        imp,
        sig: inspect.Signature = None,
        sig_annot: inspect.Signature = None,
        globals={}
    ):
        self.name = imp.__name__

        sig_annot = sig_annot or inspect.signature(imp)
        sig = sig or sig_eval_annotations(sig_annot, globals)

        self.imp = imp
        self.sig_annot = sig_annot
        self.sig = sig
        self.doc = imp.__doc__

        self.antecedents = tuple(
            Rule._param_of_parameter(p) for p in self.sig.parameters.values()
        )
        self.antecedents_annot = tuple(
            Rule._param_of_parameter(p)
            for p in self.sig_annot.parameters.values()
        )

        self.consequents = Rule._params_of_annotation(
            self.sig.return_annotation, name="<return>"
        )
        self.consequents_annot = Rule._params_of_annotation(
            self.sig_annot.return_annotation, name="<return>"
        )

    def eval(self, state: State, trace=[]) -> State:
        """
        Evaluate rule in the given state context, setting its consquents in the returned state.
        """
        for param in self.antecedents:
            if param not in state:
                raise ValueError(f"cannot evaluate rule {self} without {param}")

        # TODO: fix ordering issues
        kwargs = {
            param.name: state.get(self.antecedents[i])
            for i, param in enumerate(self.sig.parameters.values())
        }

        bindings = self.sig.bind(**kwargs)

        rets = self.imp(*bindings.args, **bindings.kwargs)

        state = state.copy()

        if len(self.consequents) == 1:
            # Single consequent implementations are not expected to return a
            # tuple and instead just produce their single consequent
            # un-containered.
            rets_as_list = [rets]
        else:
            rets_as_list = rets

        for ret, con in zip(rets_as_list, self.consequents):
            state.set(con, ret, trace=trace + [self])
            # TODO: fix tracing
            state.trace[con].append(ViaRule(self))

        return state

    # Several methods for converting a python function to a rule:

    @staticmethod
    def _param_of_parameter(param: inspect.Parameter) -> Parameter:
        if isinstance(param.annotation, str):
            return param.annotation

        if isinstance(param.annotation, Parameter):
            return param.annotation
        else:
            return Rule._param_of_annotation(param.annotation, name=param.name)

    @staticmethod
    def _param_of_annotation(annot, name) -> Parameter:
        if annot is inspect.Parameter.empty:
            return Parameter(name=name, typ=Any, doc="")
        else:
            if isinstance(annot, Parameter):
                return annot
            else:
                return Parameter(name=name, typ=annot, doc="")

    @staticmethod
    def _params_of_annotation(annot, name) -> Tuple[Parameter]:
        if isinstance(annot, Parameter):
            return tuple([annot])

        params = []

        if isinstance(annot, Iterable):
            for a in annot:
                params.append(Rule._param_of_annotation(a, name=name))
        else:
            params.append(Rule._param_of_annotation(annot, name=name))

        return tuple(params)


class InferException(Exception):
    """
    Base class for exceptions relating to rule-based inferences.
    """

    def __init__(self, msg: str, trace: Optional[List[str]] = None):
        self.msg = msg

        # TODO(piotrm): trace work ongoing
        self.trace = trace or []

    def __str__(self):
        return "\n".join(self.trace) + "\n" + self.msg

    def pileon(self, part: str) -> InferException:
        """
        Create a copy of this exception with an additional message `part` in its trace.
        """

        return InferException(self.msg, [part] + self.trace)


class NoBacktrack(InferException):
    """
    Throw this in a rule to prevent further rule evaluation.
    """
    pass


class Backtrack(InferException):
    """
    Throw this to indicate that this rule does not apply or failed but that it
    is ok to ignore this and continue with other rules that might apply.
    """
    pass


class Rules:
    """
    A collection of inference rules along with methods for performing the inference.
    """

    def __init__(self):
        self.rules = []

    def add_rule(self, rule: Rule):
        """
        Add the given `rule` to tracked collection.
        """
        self.rules.append(rule)

    def register_rules(
        self, cls: type
    ):  # TODO(piotrm): is there a better annotation for cls?
        """
        Adds all rules found in the given class `cls` to the `self.rules`
        collection. This includes all methods in that class that have a
        Parameter type in their return annotation (or an iterable of Parameter).
        """

        globals = caller_globals()

        for k in cls.__dict__.keys():
            # NOTE(piotrm): dir(cls) does NOT return contents in order of definition while __dict__ does.
            v = getattr(cls, k)
            if isinstance(v, Callable):
                try:
                    sig_annot = inspect.signature(v)
                    sig = sig_eval_annotations(sig_annot, globals)

                    ret_annot = sig.return_annotation

                    if ret_annot is not inspect.Parameter.empty:
                        if isinstance(ret_annot, Parameter) or (
                            isinstance(ret_annot, Iterable) and
                            all(isinstance(t, Parameter) for t in ret_annot)
                        ):
                            # TODO(piotrm): type printing adjustments work in progress
                            # v.__signature__ = sig

                            self.add_rule(Rule(v))

                except ValueError:
                    pass

        return cls

    def get_rules_for(self, var: Parameter) -> Iterable[Rule]:
        """
        Get all rules that have `var` in the consequents or something stronger than `var`.
        """

        for rule in self.rules:
            if any(
                State.is_stronger(consequent, var)
                for consequent in rule.consequents
            ):
                yield rule
        return

    def eval_rule(self, state: State, rule: Rule, trace=[]) -> Iterable[State]:
        """
        Evaluate the given `rule` on the given `state`, producing some number of
        resulting states.

        TODO(piotrm): `trace` work ongoing.
        """

        state = state.copy()

        # Callect all states satisfying antecedents here.
        branches = iter([])

        if all(var in state for var in rule.antecedents):
            # Have all the rule antecedants in the state. Add existing state to
            # branches as is.
            branches = chain(branches, [state])

        else:
            # Otherwise we need to infer some antecedents. There may be multiple
            # ways of doing so.
            branches = chain(
                branches,
                self.get(
                    state=state,
                    need=list(rule.antecedents),
                    optional=[],
                    trace=trace
                )
            )

        # Evaluate the rule for each antecedents branch.
        for branch in branches:
            branch_state = rule.eval(branch, trace=trace)
            yield branch_state

    @staticmethod
    def _getparameter(annot):
        if isinstance(annot, Parameter):
            return annot
        elif isinstance(annot, Given) or isinstance(annot, Optional):
            return Rules._getparameter(annot.typ)
        else:
            return None

    def bind(
        self,
        func: Function,
        state: State,
        args: Tuple[Any] = (),
        kwargs: Dict = {},
        trace=[]
    ) -> Iterable[inspect.BoundArguments]:
        """
        Produce bound arguments for the given `func` from `args` and `kwargs` or from
        things derivable from them.

        TODO(piotrm): `trace` work ongoing.
        """

        # Copy for popping.
        args: List = list(args)

        # Copy to not clobber the original.
        state = state.copy()

        # Track parameters that will need to be inferred.
        need = []

        # Track parameters that will be inferred but need not to.
        may_use = []

        sig = inspect.signature(func)

        bindings = {}

        for name, param in sig.parameters.items():
            annot = param.annotation

            annot_param = Rules._getparameter(annot)

            if annot_param is None:
                # If a parameter is not annotated as `Parameter`, treat it like in standard python.
                if param.kind is IParameter.KEYWORD_ONLY:
                    assert name in kwargs, f"Non-parameter keyword argument {name} not provided."
                    bindings[name] = kwargs[name]
                else:
                    assert len(
                        args
                    ) > 0, f"Non-parameter positional argument {name} not provided."
                    bindings[name] = args.pop(0)

                continue

            # Otherewise `annot` is `Parameter`, `Given(Parameter)`, or
            # `Optional(Parameter)`. Check if value is provided and that value
            # is not None.
            if param.kind is IParameter.KEYWORD_ONLY:
                if name in kwargs and kwargs[name] is not None:
                    state.set(annot_param, kwargs[name])
            else:
                if len(args) > 0:
                    val = args.pop(0)
                    if val is not None:
                        state.set(annot_param, val)

            # If the above failed to set a value for annot in state, make note
            # of it as needed to infer.
            if not annot_param in state:
                if isinstance(annot, Optional):
                    # Mark optional parameters as "may use" so failure to derive
                    # them is not treated as error.
                    may_use.append(annot_param)

                elif isinstance(annot, Given):
                    # Should not happen, dispatch should not be calling us if a Given-annotated parameter
                    # was not provided by user.
                    raise RuntimeError(
                        f"Was not given a value for a user-provided parameter: {annot}."
                    )
                else:  # isinstance(annot, Parameter):

                    # Things not marked with Optional must be derived.
                    need.append(annot_param)

        # Enumarate the ways in which to infer `need` from parameters set in
        # `state`. For each create the BoundArguments object which can be used
        # to call the method of interest.
        for state in self.get(
            state=state, need=need + may_use, optional=may_use, trace=trace
        ):

            for name, param in sig.parameters.items():
                annot = param.annotation
                annot_param = Rules._getparameter(annot)

                if annot_param is None:
                    # Should already be in bindings from above.
                    continue
                else:
                    assert annot_param in state, f"Do not have value for {name} in parameters state."
                    # TODO: remove this assertion once logic is certain

                    bindings[name] = state.get(annot_param)

            yield sig.bind(**bindings)

    def get(
        self,
        state: State,
        need: List[Parameter],
        optional: List[Parameter],
        trace=[]
    ) -> Iterable[State]:
        """
        Starting with `state`, use the registered rules to try to get values for
        everything in `need` list. This may be done in multiple ways hence
        produced is some number of resulting states that each should have values
        for everything in `need`. If a parameter in `need` cannot be derived,
        will not yield a state unless that parameter is also in the `optional`
        list in which case a state will be yielded with an assignment of None to
        that parameter.

        TODO(piotrm): `trace` work ongoing.
        """

        tab = "  " * len(trace)

        # TODO(piotrm): do not evaluate all rules before recurring, evaluate one at a time

        assert isinstance(need, List), f"`need` was not a list but {type(need)}"

        if len(need) == 0:
            # Nothing needed. Return state as is.
            yield state
            return

        # Will focus on the first need first, then the rest recursively.
        first, rest = need[0], need[1:]

        tab = tab + f"deriving {first}: "

        if first.name in INGESTION_CUSTOM_KEYS and "TRU_QUICK_NN_INFERENCE_FLAG" in os.environ and os.environ[
            "TRU_QUICK_NN_INFERENCE_FLAG"] == "0":
            return InferException(
                f"Inference is disabled for parameter `{first}`. "
                f"Please supply this as a parameter to the method."
            )

        # Iterator to collect a set of states that satisfy first. Will be using
        # itertools.chain to add options to this iterator.
        first_branches = iter([])

        logger.debug(tab + f"working on deriving {first}")

        if first in state:
            logger.debug(tab + "already satisfied")
            # First already satisfied.

            # First may be valid because it is already in state, or because it
            # is implied by something in state. In the first case, there is
            # nothing to do for first so append current state as is to consider
            # the rest later.

            state_copy = state.copy()
            # TODO: tracing
            # state_copy.trace[first].append(ViaInput())
            first_branches = chain(first_branches, [state_copy])

        else:
            # Note due to python weirdness, need to pass in the used variables
            # to iterator instead of assuming their value will be captured in
            # closure.
            def iter_stronger_branches(first, state, trace, tab):
                logger.debug(tab + "via stronger...")

                for stronger in state.get_stronger(first):
                    logger.debug(tab + f"via stronger {stronger}")

                    # Satisfy first via a stronger parameter.

                    # `first` is not explicitly satisfied but is implied by a
                    # parameter that is explicitly satisfied. Make a branch for each
                    # of those stronger parameters and in each branch assign the
                    # stronger parameter's value to first.

                    state_copy = state.copy()
                    state_copy.set(
                        first,
                        state_copy.get(stronger),
                        trace=trace +
                        [ViaStronger(stronger)]  # TODO: fix tracing
                    )
                    assert first in state_copy
                    logger.debug(tab + f"got {first} via {stronger}")
                    yield state_copy

                logger.debug(tab + "no more stronger")

            first_branches = chain(
                first_branches,
                iter_stronger_branches(first, state, trace, tab)
            )

            # Try to derive first using rules.
            # Create iterator for branches that use a rule so we don't
            # evaluate any of the rules until needed.
            def iter_rules_branches(first, state, trace, tab):
                logger.debug(tab + "via rules ...")

                for rule in self.get_rules_for(first):
                    # Get every rule that may be used to satisfy first.

                    if ViaRule(rule) in trace:
                        logger.debug(
                            tab + f"skipping rule {rule} since already in trace"
                        )
                        # Do not get into derivation loops which can easily occur if
                        # parameter implication has loops.
                        continue

                    logger.debug(tab + f"via rule {rule}")
                    try:
                        for branch in self.eval_rule(
                            state,
                            rule,
                            trace=trace + [ViaRule(rule)]  # TODO: fix tracing
                        ):
                            # Evaluate each rule.

                            #for branch in self.get(
                            #    _branch,
                            #    need=[first],
                            #    trace=trace + [ViaRule(rule)] # TODO: fix tracing
                            #):
                            # branch.trace[first].append(ViaRule(rule))
                            # print("first branched")
                            # And for each get a state that satisfies first. Note
                            # that the rule might have produced something that is
                            # stronger than first, so we recur to self.get to get
                            # the state which explicitly satisfies first.

                            assert first in branch, f"rule {rule} evaluation did not satisfy first {first}"

                            logger.debug(tab + f"got {first} via rule {rule}")

                            yield branch

                    except Backtrack as e:
                        logger.debug(
                            tab +
                            f"Rule {rule} wants to backtrack:\n{render_exception(e)}"
                        )
                        continue  # continue with next rule

                    except InferException as e:
                        # Re-raise the rule's exception but add onto its trace
                        # an indicator of why the failed rule was used.
                        raise e.pileon(f"Inferring {first} via {rule} ...")

                    except Exception as e:
                        raise InferException(
                            f"Rule {rule} had unexpected error:\n{retab(render_exception(e))}"
                        )

                logger.debug(tab + "no more rules")

            first_branches = chain(
                first_branches, iter_rules_branches(first, state, trace, tab)
            )

        yielded_something = False

        logger.debug(tab + f"enumerating branches for {first}")

        # Try to satisfy the rest of the parameters for each of the ways in
        # which first can be satisfied.
        for branch in first_branches:
            assert first in branch, f"first {first} was not yet satisfied when considering rest {rest}"

            logger.debug(tab + f"current branch={branch}")

            if len(rest) == 0:
                logger.debug(
                    tab + "nothing else to infer, yielding current branch"
                )
                yielded_something = True
                yield branch
            else:
                logger.debug(tab + f"continuing with rest={rest}")
                for state in self.get(
                    state=branch, need=rest, optional=optional, trace=trace
                ):
                    yielded_something = True
                    yield state

        if not yielded_something:
            if first in optional:
                # `first` could not be derived but it is optional so assign None
                # to it and continue with rest. Note that this will not trigger
                # if there was a valid inference for `first`. That is, the None
                # value is not considered a branch but rather an alterative to a
                # case where there are no branches for it.

                print(
                    f"WARNING: optional parameter {first} could not be inferred"
                )

                branch = state.copy()
                branch.set(first, None)

                if len(rest) == 0:
                    logger.debug(
                        tab + "nothing else to infer, yielding current branch"
                    )
                    yielded_something = True
                    yield branch
                else:
                    logger.debug(tab + f"continuing with rest={rest}")
                    for state in self.get(
                        state=branch, need=rest, optional=optional, trace=trace
                    ):
                        yielded_something = True
                        yield state

            else:
                # Create a message indicating a derivation failure if the above
                # yielded nothing for `first` and `first` was not optional.
                message = f"No way to infer {first}.\n"
                # message += f"trace={trace}\n"
                message += f"Have:\n" + retab(str(state))

                raise Backtrack(message, trace=[f"Inferring {first} ..."])
