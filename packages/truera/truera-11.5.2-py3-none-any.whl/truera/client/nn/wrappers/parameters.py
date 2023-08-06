import inspect
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

from truera.client.nn.client_configs import LayerAnchor
from truera.client.nn.wrappers.nlp import Wrappers as NLP
from truera.client.util.types import Function
from truera.client.util.types import Intersection
from truera.client.util.types import Parameter
from truera.client.util.types import TypeMatching
from truera.client.util.types import Union

PTokenizerWrapper = Parameter(
    "tokenizer_wrapper", doc="Tokenizer wrapper", typ=NLP.TokenizerWrapper
)
PModelLoadWrapper = Parameter(
    "model_load_wrapper", doc="Model load wrapper", typ=NLP.ModelLoadWrapper
)
PModelRunWrapper = Parameter(
    "model_run_wrapper", doc="Model run wrapper", typ=NLP.ModelRunWrapper
)
PSplitLoadWrapper = Parameter(
    "split_load_wrapper", doc="Split load wrapper", typ=NLP.SplitLoadWrapper
)


# Here only for its signature:
def example_model(*args, **kwargs) -> Any:
    ...


TBlackboxModel = Function(inspect.signature(example_model))
PModelBlackbox = Parameter("model", typ=TBlackboxModel, doc="Blackbox model.")

TTorchModel = 'torch.nn.Module'
TTF1Model = 'tensorflow.Graph'
TTF2Model = Union(
    'keras.engine.training.Model', 'tensorflow.keras.Model',
    'tensorflow_hub.keras_layer.KerasLayer', 'tensorflow.estimator.Estimator'
)

PModel = Parameter(
    "model",
    typ=Union(TTorchModel, TTF1Model, TTF2Model, TBlackboxModel),
    doc="A Model."
)

PModelTorch = Parameter("model", typ=TTorchModel, doc="A pytorch model.")
PModelTF1 = Parameter("model", typ=TTF1Model, doc="A tensorflow 1 model.")
PModelTF2 = Parameter("model", typ=TTF2Model, doc="A tensorflow 2 model.")

PHuggingfaceModelName = Parameter(
    "model_name", typ=str, doc="A Huggingface model name."
)

# Huggingface base model classes. These are the ones that would be included as
# part of a feature extractor followed by a classifier architecture.
# Output of:
#print(concretize(
#    transformers.models, pattern=re.compile(r"transformers\..+Model")
#))
PModelHugsBase = Parameter(
    "model",
    doc="Base huggingface model.",
    typ=Union(
        'transformers.models.albert.modeling_albert.AlbertModel',
        'transformers.models.albert.modeling_albert.AlbertPreTrainedModel',
        'transformers.modeling_utils.PreTrainedModel',
        'transformers.models.auto.modeling_auto.AutoModel',
        'transformers.models.bart.modeling_bart.BartModel',
        'transformers.models.bart.modeling_bart.BartPretrainedModel',
        'transformers.models.bart.modeling_bart.PretrainedBartModel',
        'transformers.models.beit.modeling_beit.BeitModel',
        'transformers.models.beit.modeling_beit.BeitPreTrainedModel',
        'transformers.models.bert.modeling_bert.BertLMHeadModel',
        'transformers.models.bert.modeling_bert.BertModel',
        'transformers.models.bert.modeling_bert.BertPreTrainedModel',
        'transformers.models.bert_generation.modeling_bert_generation.BertGenerationPreTrainedModel',
        'transformers.models.big_bird.modeling_big_bird.BigBirdModel',
        'transformers.models.big_bird.modeling_big_bird.BigBirdPreTrainedModel',
        'transformers.models.bigbird_pegasus.modeling_bigbird_pegasus.BigBirdPegasusModel',
        'transformers.models.bigbird_pegasus.modeling_bigbird_pegasus.BigBirdPegasusPreTrainedModel',
        'transformers.models.blenderbot.modeling_blenderbot.BlenderbotModel',
        'transformers.models.blenderbot.modeling_blenderbot.BlenderbotPreTrainedModel',
        'transformers.models.blenderbot_small.modeling_blenderbot_small.BlenderbotSmallModel',
        'transformers.models.blenderbot_small.modeling_blenderbot_small.BlenderbotSmallPreTrainedModel',
        'transformers.models.bloom.modeling_bloom.BloomModel',
        'transformers.models.bloom.modeling_bloom.BloomPreTrainedModel',
        'transformers.models.camembert.modeling_camembert.CamembertModel',
        'transformers.models.roberta.modeling_roberta.RobertaModel',
        'transformers.models.canine.modeling_canine.CanineModel',
        'transformers.models.canine.modeling_canine.CaninePreTrainedModel',
        'transformers.models.clip.modeling_clip.CLIPModel',
        'transformers.models.clip.modeling_clip.CLIPPreTrainedModel',
        'transformers.models.clip.modeling_clip.CLIPTextModel',
        'transformers.models.clip.modeling_clip.CLIPVisionModel',
        'transformers.models.codegen.modeling_codegen.CodeGenModel',
        'transformers.models.codegen.modeling_codegen.CodeGenPreTrainedModel',
        'transformers.models.convbert.modeling_convbert.ConvBertModel',
        'transformers.models.convbert.modeling_convbert.ConvBertPreTrainedModel',
        'transformers.models.convnext.modeling_convnext.ConvNextModel',
        'transformers.models.convnext.modeling_convnext.ConvNextPreTrainedModel',
        'transformers.models.ctrl.modeling_ctrl.CTRLLMHeadModel',
        'transformers.models.ctrl.modeling_ctrl.CTRLModel',
        'transformers.models.ctrl.modeling_ctrl.CTRLPreTrainedModel',
        'transformers.models.cvt.modeling_cvt.CvtModel',
        'transformers.models.cvt.modeling_cvt.CvtPreTrainedModel',
        'transformers.models.data2vec.modeling_data2vec_audio.Data2VecAudioModel',
        'transformers.models.data2vec.modeling_data2vec_audio.Data2VecAudioPreTrainedModel',
        'transformers.models.data2vec.modeling_data2vec_text.Data2VecTextModel',
        'transformers.models.data2vec.modeling_data2vec_text.Data2VecTextPreTrainedModel',
        'transformers.models.data2vec.modeling_data2vec_vision.Data2VecVisionModel',
        'transformers.models.data2vec.modeling_data2vec_vision.Data2VecVisionPreTrainedModel',
        'transformers.models.deberta.modeling_deberta.DebertaModel',
        'transformers.models.deberta.modeling_deberta.DebertaPreTrainedModel',
        'transformers.models.deberta_v2.modeling_deberta_v2.DebertaV2Model',
        'transformers.models.deberta_v2.modeling_deberta_v2.DebertaV2PreTrainedModel',
        'transformers.models.decision_transformer.modeling_decision_transformer.DecisionTransformerGPT2Model',
        'transformers.models.decision_transformer.modeling_decision_transformer.DecisionTransformerGPT2PreTrainedModel',
        'transformers.models.decision_transformer.modeling_decision_transformer.DecisionTransformerModel',
        'transformers.models.decision_transformer.modeling_decision_transformer.DecisionTransformerPreTrainedModel',
        'transformers.models.deit.modeling_deit.DeiTModel',
        'transformers.models.deit.modeling_deit.DeiTPreTrainedModel',
        'transformers.models.distilbert.modeling_distilbert.DistilBertModel',
        'transformers.models.distilbert.modeling_distilbert.DistilBertPreTrainedModel',
        'transformers.models.donut.modeling_donut_swin.DonutSwinModel',
        'transformers.models.donut.modeling_donut_swin.DonutSwinPreTrainedModel',
        'transformers.models.dpr.modeling_dpr.DPRPreTrainedModel',
        'transformers.models.dpt.modeling_dpt.DPTModel',
        'transformers.models.dpt.modeling_dpt.DPTPreTrainedModel',
        'transformers.models.electra.modeling_electra.ElectraModel',
        'transformers.models.electra.modeling_electra.ElectraPreTrainedModel',
        'transformers.models.encoder_decoder.modeling_encoder_decoder.EncoderDecoderModel',
        'transformers.models.ernie.modeling_ernie.ErnieModel',
        'transformers.models.ernie.modeling_ernie.ErniePreTrainedModel',
        'transformers.models.flaubert.modeling_flaubert.FlaubertModel',
        'transformers.models.flaubert.modeling_flaubert.FlaubertWithLMHeadModel',
        'transformers.models.xlm.modeling_xlm.XLMModel',
        'transformers.models.xlm.modeling_xlm.XLMWithLMHeadModel',
        'transformers.models.flava.modeling_flava.FlavaImageModel',
        'transformers.models.flava.modeling_flava.FlavaModel',
        'transformers.models.flava.modeling_flava.FlavaMultimodalModel',
        'transformers.models.flava.modeling_flava.FlavaPreTrainedModel',
        'transformers.models.flava.modeling_flava.FlavaTextModel',
        'transformers.models.fnet.modeling_fnet.FNetModel',
        'transformers.models.fnet.modeling_fnet.FNetPreTrainedModel',
        'transformers.models.fsmt.modeling_fsmt.FSMTModel',
        'transformers.models.fsmt.modeling_fsmt.PretrainedFSMTModel',
        'transformers.models.funnel.modeling_funnel.FunnelBaseModel',
        'transformers.models.funnel.modeling_funnel.FunnelModel',
        'transformers.models.funnel.modeling_funnel.FunnelPreTrainedModel',
        'transformers.models.glpn.modeling_glpn.GLPNModel',
        'transformers.models.glpn.modeling_glpn.GLPNPreTrainedModel',
        'transformers.models.gpt2.modeling_gpt2.GPT2DoubleHeadsModel',
        'transformers.models.gpt2.modeling_gpt2.GPT2LMHeadModel',
        'transformers.models.gpt2.modeling_gpt2.GPT2Model',
        'transformers.models.gpt2.modeling_gpt2.GPT2PreTrainedModel',
        'transformers.models.gpt_neo.modeling_gpt_neo.GPTNeoModel',
        'transformers.models.gpt_neo.modeling_gpt_neo.GPTNeoPreTrainedModel',
        'transformers.models.gpt_neox.modeling_gpt_neox.GPTNeoXModel',
        'transformers.models.gpt_neox.modeling_gpt_neox.GPTNeoXPreTrainedModel',
        'transformers.models.gptj.modeling_gptj.GPTJModel',
        'transformers.models.gptj.modeling_gptj.GPTJPreTrainedModel',
        'transformers.models.groupvit.modeling_groupvit.GroupViTModel',
        'transformers.models.groupvit.modeling_groupvit.GroupViTPreTrainedModel',
        'transformers.models.groupvit.modeling_groupvit.GroupViTTextModel',
        'transformers.models.groupvit.modeling_groupvit.GroupViTVisionModel',
        'transformers.models.hubert.modeling_hubert.HubertModel',
        'transformers.models.hubert.modeling_hubert.HubertPreTrainedModel',
        'transformers.models.ibert.modeling_ibert.IBertModel',
        'transformers.models.ibert.modeling_ibert.IBertPreTrainedModel',
        'transformers.models.imagegpt.modeling_imagegpt.ImageGPTModel',
        'transformers.models.imagegpt.modeling_imagegpt.ImageGPTPreTrainedModel',
        'transformers.models.layoutlm.modeling_layoutlm.LayoutLMModel',
        'transformers.models.layoutlm.modeling_layoutlm.LayoutLMPreTrainedModel',
        'transformers.models.layoutlmv2.modeling_layoutlmv2.LayoutLMv2Model',
        'transformers.models.layoutlmv2.modeling_layoutlmv2.LayoutLMv2PreTrainedModel',
        'transformers.models.layoutlmv3.modeling_layoutlmv3.LayoutLMv3Model',
        'transformers.models.layoutlmv3.modeling_layoutlmv3.LayoutLMv3PreTrainedModel',
        'transformers.models.led.modeling_led.LEDModel',
        'transformers.models.led.modeling_led.LEDPreTrainedModel',
        'transformers.models.levit.modeling_levit.LevitModel',
        'transformers.models.levit.modeling_levit.LevitPreTrainedModel',
        'transformers.models.longformer.modeling_longformer.LongformerModel',
        'transformers.models.longformer.modeling_longformer.LongformerPreTrainedModel',
        'transformers.models.longt5.modeling_longt5.LongT5EncoderModel',
        'transformers.models.longt5.modeling_longt5.LongT5Model',
        'transformers.models.longt5.modeling_longt5.LongT5PreTrainedModel',
        'transformers.models.luke.modeling_luke.LukeModel',
        'transformers.models.luke.modeling_luke.LukePreTrainedModel',
        'transformers.models.lxmert.modeling_lxmert.LxmertModel',
        'transformers.models.lxmert.modeling_lxmert.LxmertPreTrainedModel',
        'transformers.models.m2m_100.modeling_m2m_100.M2M100Model',
        'transformers.models.m2m_100.modeling_m2m_100.M2M100PreTrainedModel',
        'transformers.models.marian.modeling_marian.MarianMTModel',
        'transformers.models.marian.modeling_marian.MarianModel',
        'transformers.models.marian.modeling_marian.MarianPreTrainedModel',
        'transformers.models.maskformer.modeling_maskformer.MaskFormerModel',
        'transformers.models.maskformer.modeling_maskformer.MaskFormerPreTrainedModel',
        'transformers.models.maskformer.modeling_maskformer.MaskFormerFPNModel',
        'transformers.models.maskformer.modeling_maskformer.MaskFormerSwinModel',
        'transformers.models.mbart.modeling_mbart.MBartModel',
        'transformers.models.mbart.modeling_mbart.MBartPreTrainedModel',
        'transformers.models.mctct.modeling_mctct.MCTCTModel',
        'transformers.models.mctct.modeling_mctct.MCTCTPreTrainedModel',
        'transformers.models.megatron_bert.modeling_megatron_bert.MegatronBertModel',
        'transformers.models.megatron_bert.modeling_megatron_bert.MegatronBertPreTrainedModel',
        'transformers.models.mmbt.modeling_mmbt.MMBTModel',
        'transformers.models.mobilebert.modeling_mobilebert.MobileBertModel',
        'transformers.models.mobilebert.modeling_mobilebert.MobileBertPreTrainedModel',
        'transformers.models.mobilevit.modeling_mobilevit.MobileViTModel',
        'transformers.models.mobilevit.modeling_mobilevit.MobileViTPreTrainedModel',
        'transformers.models.mpnet.modeling_mpnet.MPNetModel',
        'transformers.models.mpnet.modeling_mpnet.MPNetPreTrainedModel',
        'transformers.models.mt5.modeling_mt5.MT5EncoderModel',
        'transformers.models.mt5.modeling_mt5.MT5Model',
        'transformers.models.t5.modeling_t5.T5EncoderModel',
        'transformers.models.t5.modeling_t5.T5Model',
        'transformers.models.mvp.modeling_mvp.MvpModel',
        'transformers.models.mvp.modeling_mvp.MvpPreTrainedModel',
        'transformers.models.nezha.modeling_nezha.NezhaModel',
        'transformers.models.nezha.modeling_nezha.NezhaPreTrainedModel',
        'transformers.models.nystromformer.modeling_nystromformer.NystromformerModel',
        'transformers.models.nystromformer.modeling_nystromformer.NystromformerPreTrainedModel',
        'transformers.models.openai.modeling_openai.OpenAIGPTDoubleHeadsModel',
        'transformers.models.openai.modeling_openai.OpenAIGPTLMHeadModel',
        'transformers.models.openai.modeling_openai.OpenAIGPTModel',
        'transformers.models.openai.modeling_openai.OpenAIGPTPreTrainedModel',
        'transformers.models.opt.modeling_opt.OPTModel',
        'transformers.models.opt.modeling_opt.OPTPreTrainedModel',
        'transformers.models.owlvit.modeling_owlvit.OwlViTModel',
        'transformers.models.owlvit.modeling_owlvit.OwlViTPreTrainedModel',
        'transformers.models.owlvit.modeling_owlvit.OwlViTTextModel',
        'transformers.models.owlvit.modeling_owlvit.OwlViTVisionModel',
        'transformers.models.pegasus.modeling_pegasus.PegasusModel',
        'transformers.models.pegasus.modeling_pegasus.PegasusPreTrainedModel',
        'transformers.models.pegasus_x.modeling_pegasus_x.PegasusXModel',
        'transformers.models.pegasus_x.modeling_pegasus_x.PegasusXPreTrainedModel',
        'transformers.models.perceiver.modeling_perceiver.PerceiverModel',
        'transformers.models.perceiver.modeling_perceiver.PerceiverPreTrainedModel',
        'transformers.models.plbart.modeling_plbart.PLBartModel',
        'transformers.models.plbart.modeling_plbart.PLBartPreTrainedModel',
        'transformers.models.poolformer.modeling_poolformer.PoolFormerModel',
        'transformers.models.poolformer.modeling_poolformer.PoolFormerPreTrainedModel',
        'transformers.models.prophetnet.modeling_prophetnet.ProphetNetModel',
        'transformers.models.prophetnet.modeling_prophetnet.ProphetNetPreTrainedModel',
        'transformers.models.qdqbert.modeling_qdqbert.QDQBertLMHeadModel',
        'transformers.models.qdqbert.modeling_qdqbert.QDQBertModel',
        'transformers.models.qdqbert.modeling_qdqbert.QDQBertPreTrainedModel',
        'transformers.models.rag.modeling_rag.RagModel',
        'transformers.models.rag.modeling_rag.RagPreTrainedModel',
        'transformers.models.realm.modeling_realm.RealmPreTrainedModel',
        'transformers.models.realm.modeling_realm.RealmBertModel',
        'transformers.models.reformer.modeling_reformer.ReformerModel',
        'transformers.models.reformer.modeling_reformer.ReformerPreTrainedModel',
        'transformers.models.regnet.modeling_regnet.RegNetModel',
        'transformers.models.regnet.modeling_regnet.RegNetPreTrainedModel',
        'transformers.models.rembert.modeling_rembert.RemBertModel',
        'transformers.models.rembert.modeling_rembert.RemBertPreTrainedModel',
        'transformers.models.resnet.modeling_resnet.ResNetModel',
        'transformers.models.resnet.modeling_resnet.ResNetPreTrainedModel',
        'transformers.models.retribert.modeling_retribert.RetriBertModel',
        'transformers.models.retribert.modeling_retribert.RetriBertPreTrainedModel',
        'transformers.models.roberta.modeling_roberta.RobertaPreTrainedModel',
        'transformers.models.roformer.modeling_roformer.RoFormerModel',
        'transformers.models.roformer.modeling_roformer.RoFormerPreTrainedModel',
        'transformers.models.segformer.modeling_segformer.SegformerModel',
        'transformers.models.segformer.modeling_segformer.SegformerPreTrainedModel',
        'transformers.models.sew.modeling_sew.SEWModel',
        'transformers.models.sew.modeling_sew.SEWPreTrainedModel',
        'transformers.models.sew_d.modeling_sew_d.SEWDModel',
        'transformers.models.sew_d.modeling_sew_d.SEWDPreTrainedModel',
        'transformers.models.speech_encoder_decoder.modeling_speech_encoder_decoder.SpeechEncoderDecoderModel',
        'transformers.models.speech_to_text.modeling_speech_to_text.Speech2TextModel',
        'transformers.models.speech_to_text.modeling_speech_to_text.Speech2TextPreTrainedModel',
        'transformers.models.speech_to_text_2.modeling_speech_to_text_2.Speech2Text2PreTrainedModel',
        'transformers.models.splinter.modeling_splinter.SplinterModel',
        'transformers.models.splinter.modeling_splinter.SplinterPreTrainedModel',
        'transformers.models.squeezebert.modeling_squeezebert.SqueezeBertModel',
        'transformers.models.squeezebert.modeling_squeezebert.SqueezeBertPreTrainedModel',
        'transformers.models.swin.modeling_swin.SwinModel',
        'transformers.models.swin.modeling_swin.SwinPreTrainedModel',
        'transformers.models.swinv2.modeling_swinv2.Swinv2Model',
        'transformers.models.swinv2.modeling_swinv2.Swinv2PreTrainedModel',
        'transformers.models.t5.modeling_t5.T5PreTrainedModel',
        'transformers.models.tapas.modeling_tapas.TapasModel',
        'transformers.models.tapas.modeling_tapas.TapasPreTrainedModel',
        'transformers.models.trajectory_transformer.modeling_trajectory_transformer.TrajectoryTransformerModel',
        'transformers.models.trajectory_transformer.modeling_trajectory_transformer.TrajectoryTransformerPreTrainedModel',
        'transformers.models.transfo_xl.modeling_transfo_xl.TransfoXLLMHeadModel',
        'transformers.models.transfo_xl.modeling_transfo_xl.TransfoXLModel',
        'transformers.models.transfo_xl.modeling_transfo_xl.TransfoXLPreTrainedModel',
        'transformers.models.trocr.modeling_trocr.TrOCRPreTrainedModel',
        'transformers.models.unispeech.modeling_unispeech.UniSpeechModel',
        'transformers.models.unispeech.modeling_unispeech.UniSpeechPreTrainedModel',
        'transformers.models.unispeech_sat.modeling_unispeech_sat.UniSpeechSatModel',
        'transformers.models.unispeech_sat.modeling_unispeech_sat.UniSpeechSatPreTrainedModel',
        'transformers.models.van.modeling_van.VanModel',
        'transformers.models.van.modeling_van.VanPreTrainedModel',
        'transformers.models.videomae.modeling_videomae.VideoMAEModel',
        'transformers.models.videomae.modeling_videomae.VideoMAEPreTrainedModel',
        'transformers.models.vilt.modeling_vilt.ViltModel',
        'transformers.models.vilt.modeling_vilt.ViltPreTrainedModel',
        'transformers.models.vision_encoder_decoder.modeling_vision_encoder_decoder.VisionEncoderDecoderModel',
        'transformers.models.vision_text_dual_encoder.modeling_vision_text_dual_encoder.VisionTextDualEncoderModel',
        'transformers.models.visual_bert.modeling_visual_bert.VisualBertModel',
        'transformers.models.visual_bert.modeling_visual_bert.VisualBertPreTrainedModel',
        'transformers.models.vit.modeling_vit.ViTModel',
        'transformers.models.vit.modeling_vit.ViTPreTrainedModel',
        'transformers.models.vit_mae.modeling_vit_mae.ViTMAEModel',
        'transformers.models.vit_mae.modeling_vit_mae.ViTMAEPreTrainedModel',
        'transformers.models.wav2vec2.modeling_wav2vec2.Wav2Vec2Model',
        'transformers.models.wav2vec2.modeling_wav2vec2.Wav2Vec2PreTrainedModel',
        'transformers.models.wav2vec2_conformer.modeling_wav2vec2_conformer.Wav2Vec2ConformerModel',
        'transformers.models.wav2vec2_conformer.modeling_wav2vec2_conformer.Wav2Vec2ConformerPreTrainedModel',
        'transformers.models.wavlm.modeling_wavlm.WavLMModel',
        'transformers.models.wavlm.modeling_wavlm.WavLMPreTrainedModel',
        'transformers.models.x_clip.modeling_x_clip.XCLIPModel',
        'transformers.models.x_clip.modeling_x_clip.XCLIPPreTrainedModel',
        'transformers.models.x_clip.modeling_x_clip.XCLIPTextModel',
        'transformers.models.x_clip.modeling_x_clip.XCLIPVisionModel',
        'transformers.models.xglm.modeling_xglm.XGLMModel',
        'transformers.models.xglm.modeling_xglm.XGLMPreTrainedModel',
        'transformers.models.xlm.modeling_xlm.XLMPreTrainedModel',
        'transformers.models.xlm_prophetnet.modeling_xlm_prophetnet.XLMProphetNetModel',
        'transformers.models.xlm_roberta.modeling_xlm_roberta.XLMRobertaModel',
        'transformers.models.xlm_roberta_xl.modeling_xlm_roberta_xl.XLMRobertaXLModel',
        'transformers.models.xlm_roberta_xl.modeling_xlm_roberta_xl.XLMRobertaXLPreTrainedModel',
        'transformers.models.xlnet.modeling_xlnet.XLNetLMHeadModel',
        'transformers.models.xlnet.modeling_xlnet.XLNetModel',
        'transformers.models.xlnet.modeling_xlnet.XLNetPreTrainedModel',
        'transformers.models.yolos.modeling_yolos.YolosModel',
        'transformers.models.yolos.modeling_yolos.YolosPreTrainedModel',
        'transformers.models.yoso.modeling_yoso.YosoModel',
        'transformers.models.yoso.modeling_yoso.YosoPreTrainedModel'
    )
)

# Huggingface sequence classifiers.
# Output of:
# print(concretize(
#    transformers.models, pattern=re.compile(r"transformers\..+ForSequenceClassification")
# ))
TModelHugsClassifier = Union(
    'transformers.models.albert.modeling_albert.AlbertForSequenceClassification',
    'transformers.models.albert.modeling_tf_albert.TFAlbertForSequenceClassification',
    # 'transformers.models.auto.modeling_auto.AutoModelForSequenceClassification',
    # 'transformers.models.auto.modeling_tf_auto.TFAutoModelForSequenceClassification',
    # NOTE(piotrm): The above "auto" classes are not models themselves.
    'transformers.models.bart.modeling_bart.BartForSequenceClassification',
    'transformers.models.bert.modeling_bert.BertForSequenceClassification',
    'transformers.models.bert.modeling_tf_bert.TFBertForSequenceClassification',
    'transformers.models.big_bird.modeling_big_bird.BigBirdForSequenceClassification',
    'transformers.models.bigbird_pegasus.modeling_bigbird_pegasus.BigBirdPegasusForSequenceClassification',
    'transformers.models.bloom.modeling_bloom.BloomForSequenceClassification',
    'transformers.models.camembert.modeling_camembert.CamembertForSequenceClassification',
    'transformers.models.camembert.modeling_tf_camembert.TFCamembertForSequenceClassification',
    'transformers.models.canine.modeling_canine.CanineForSequenceClassification',
    'transformers.models.convbert.modeling_convbert.ConvBertForSequenceClassification',
    'transformers.models.convbert.modeling_tf_convbert.TFConvBertForSequenceClassification',
    'transformers.models.ctrl.modeling_ctrl.CTRLForSequenceClassification',
    'transformers.models.ctrl.modeling_tf_ctrl.TFCTRLForSequenceClassification',
    'transformers.models.data2vec.modeling_data2vec_audio.Data2VecAudioForSequenceClassification',
    'transformers.models.data2vec.modeling_data2vec_text.Data2VecTextForSequenceClassification',
    'transformers.models.deberta.modeling_deberta.DebertaForSequenceClassification',
    'transformers.models.deberta.modeling_tf_deberta.TFDebertaForSequenceClassification',
    'transformers.models.deberta_v2.modeling_deberta_v2.DebertaV2ForSequenceClassification',
    'transformers.models.deberta_v2.modeling_tf_deberta_v2.TFDebertaV2ForSequenceClassification',
    'transformers.models.distilbert.modeling_distilbert.DistilBertForSequenceClassification',
    'transformers.models.distilbert.modeling_tf_distilbert.TFDistilBertForSequenceClassification',
    'transformers.models.electra.modeling_electra.ElectraForSequenceClassification',
    'transformers.models.electra.modeling_tf_electra.TFElectraForSequenceClassification',
    'transformers.models.ernie.modeling_ernie.ErnieForSequenceClassification',
    'transformers.models.esm.modeling_esm.EsmForSequenceClassification',
    'transformers.models.flaubert.modeling_flaubert.FlaubertForSequenceClassification',
    'transformers.models.flaubert.modeling_tf_flaubert.TFFlaubertForSequenceClassification',
    'transformers.models.xlm.modeling_xlm.XLMForSequenceClassification',
    'transformers.models.xlm.modeling_tf_xlm.TFXLMForSequenceClassification',
    'transformers.models.fnet.modeling_fnet.FNetForSequenceClassification',
    'transformers.models.funnel.modeling_funnel.FunnelForSequenceClassification',
    'transformers.models.funnel.modeling_tf_funnel.TFFunnelForSequenceClassification',
    'transformers.models.gpt2.modeling_gpt2.GPT2ForSequenceClassification',
    'transformers.models.gpt2.modeling_tf_gpt2.TFGPT2ForSequenceClassification',
    'transformers.models.gpt_neo.modeling_gpt_neo.GPTNeoForSequenceClassification',
    'transformers.models.gptj.modeling_gptj.GPTJForSequenceClassification',
    'transformers.models.gptj.modeling_tf_gptj.TFGPTJForSequenceClassification',
    'transformers.models.hubert.modeling_hubert.HubertForSequenceClassification',
    'transformers.models.ibert.modeling_ibert.IBertForSequenceClassification',
    'transformers.models.layoutlm.modeling_layoutlm.LayoutLMForSequenceClassification',
    'transformers.models.layoutlm.modeling_tf_layoutlm.TFLayoutLMForSequenceClassification',
    'transformers.models.layoutlmv2.modeling_layoutlmv2.LayoutLMv2ForSequenceClassification',
    'transformers.models.layoutlmv3.modeling_layoutlmv3.LayoutLMv3ForSequenceClassification',
    'transformers.models.layoutlmv3.modeling_tf_layoutlmv3.TFLayoutLMv3ForSequenceClassification',
    'transformers.models.led.modeling_led.LEDForSequenceClassification',
    'transformers.models.longformer.modeling_longformer.LongformerForSequenceClassification',
    'transformers.models.longformer.modeling_tf_longformer.TFLongformerForSequenceClassification',
    'transformers.models.luke.modeling_luke.LukeForSequenceClassification',
    'transformers.models.markuplm.modeling_markuplm.MarkupLMForSequenceClassification',
    'transformers.models.mbart.modeling_mbart.MBartForSequenceClassification',
    'transformers.models.megatron_bert.modeling_megatron_bert.MegatronBertForSequenceClassification',
    'transformers.models.mobilebert.modeling_mobilebert.MobileBertForSequenceClassification',
    'transformers.models.mobilebert.modeling_tf_mobilebert.TFMobileBertForSequenceClassification',
    'transformers.models.mpnet.modeling_mpnet.MPNetForSequenceClassification',
    'transformers.models.mpnet.modeling_tf_mpnet.TFMPNetForSequenceClassification',
    'transformers.models.mvp.modeling_mvp.MvpForSequenceClassification',
    'transformers.models.nezha.modeling_nezha.NezhaForSequenceClassification',
    'transformers.models.nystromformer.modeling_nystromformer.NystromformerForSequenceClassification',
    'transformers.models.openai.modeling_openai.OpenAIGPTForSequenceClassification',
    'transformers.models.openai.modeling_tf_openai.TFOpenAIGPTForSequenceClassification',
    'transformers.models.opt.modeling_opt.OPTForSequenceClassification',
    'transformers.models.perceiver.modeling_perceiver.PerceiverForSequenceClassification',
    'transformers.models.plbart.modeling_plbart.PLBartForSequenceClassification',
    'transformers.models.qdqbert.modeling_qdqbert.QDQBertForSequenceClassification',
    'transformers.models.reformer.modeling_reformer.ReformerForSequenceClassification',
    'transformers.models.rembert.modeling_rembert.RemBertForSequenceClassification',
    'transformers.models.rembert.modeling_tf_rembert.TFRemBertForSequenceClassification',
    'transformers.models.roberta.modeling_roberta.RobertaForSequenceClassification',
    'transformers.models.roberta.modeling_tf_roberta.TFRobertaForSequenceClassification',
    'transformers.models.roformer.modeling_roformer.RoFormerForSequenceClassification',
    'transformers.models.roformer.modeling_tf_roformer.TFRoFormerForSequenceClassification',
    'transformers.models.sew.modeling_sew.SEWForSequenceClassification',
    'transformers.models.sew_d.modeling_sew_d.SEWDForSequenceClassification',
    'transformers.models.squeezebert.modeling_squeezebert.SqueezeBertForSequenceClassification',
    'transformers.models.tapas.modeling_tf_tapas.TFTapasForSequenceClassification',
    'transformers.models.tapas.modeling_tapas.TapasForSequenceClassification',
    'transformers.models.transfo_xl.modeling_tf_transfo_xl.TFTransfoXLForSequenceClassification',
    'transformers.models.transfo_xl.modeling_transfo_xl.TransfoXLForSequenceClassification',
    'transformers.models.unispeech.modeling_unispeech.UniSpeechForSequenceClassification',
    'transformers.models.unispeech_sat.modeling_unispeech_sat.UniSpeechSatForSequenceClassification',
    'transformers.models.wav2vec2.modeling_wav2vec2.Wav2Vec2ForSequenceClassification',
    'transformers.models.wav2vec2_conformer.modeling_wav2vec2_conformer.Wav2Vec2ConformerForSequenceClassification',
    'transformers.models.wavlm.modeling_wavlm.WavLMForSequenceClassification',
    'transformers.models.xlm_roberta.modeling_tf_xlm_roberta.TFXLMRobertaForSequenceClassification',
    'transformers.models.xlm_roberta.modeling_xlm_roberta.XLMRobertaForSequenceClassification',
    'transformers.models.xlm_roberta_xl.modeling_xlm_roberta_xl.XLMRobertaXLForSequenceClassification',
    'transformers.models.xlnet.modeling_tf_xlnet.TFXLNetForSequenceClassification',
    'transformers.models.xlnet.modeling_xlnet.XLNetForSequenceClassification',
    'transformers.models.yoso.modeling_yoso.YosoForSequenceClassification'
)

PModelHugsClassifier = Parameter(
    "model", typ=Intersection(PModel, TModelHugsClassifier), doc=""
)

# Huggingface audio sequence classifiers
TModelHugsAudioClassifierPattern = TypeMatching(
    pattern=
    "transformers\..+(UniSpeech|Audio|WavLM|Wav2Vec2).*ForSequenceClassification"
)
# print(concretize(
#    transformers.models,
#    TModelHugsAudioClassifierPattern
# ))
TModelHugsAudioClassifier = Union(
    'transformers.models.data2vec.modeling_data2vec_audio.Data2VecAudioForSequenceClassification',
    'transformers.models.unispeech.modeling_unispeech.UniSpeechForSequenceClassification',
    'transformers.models.unispeech_sat.modeling_unispeech_sat.UniSpeechSatForSequenceClassification',
    'transformers.models.wav2vec2.modeling_wav2vec2.Wav2Vec2ForSequenceClassification',
    'transformers.models.wav2vec2_conformer.modeling_wav2vec2_conformer.Wav2Vec2ConformerForSequenceClassification',
    'transformers.models.wavlm.modeling_wavlm.WavLMForSequenceClassification'
)

PModelHugsAudioClassifier = Parameter(
    "model",
    typ=Intersection(PModel, TModelHugsAudioClassifier),
    doc="Audio classifier. These are not yet supperted."
)

# Huggingface text sequence classifiers. NOTE(piotrm): Not using the "Not" type
# constructor here intentionally as doing so requires enabling very slow
# subclass checking.
PModelHugsTextClassifier = Parameter(
    "model",
    typ=Union(
        *(
            t for t in TModelHugsClassifier.types
            if t not in TModelHugsAudioClassifier.types
        )
    ),
    doc=""
)

# Huggingface (text?) tokenizers
TTokenizerHugs = Union(
    'transformers.PreTrainedTokenizer', 'transformers.PreTrainedTokenizerFast'
)
TKerasTextVectorizationTokenizer = "tensorflow.keras.layers.TextVectorization"
TTFTextTokenizer = "tensorflow_text.Tokenizer"
TTFTextTokenizerWithOffsets = "tensorflow_text.TokenizerWithOffsets"
TTFTextBertTokenizer = "tensorflow_text.BertTokenizer"

TTF2Tokenizer = Union(
    TKerasTextVectorizationTokenizer, TTFTextTokenizer,
    TTFTextTokenizerWithOffsets, TTFTextBertTokenizer, TTF2Model
)


def example_tokenizer(*args, **kwargs) -> Any:
    ...


TBlackboxTokenizer = Function(inspect.signature(example_tokenizer))

PTokenizerHugs = Parameter("tokenizer", typ=TTokenizerHugs, doc="")

PKerasTextVectorizationTokenizer = Parameter(
    "tokenizer", typ=TKerasTextVectorizationTokenizer, doc=""
)

PTFTextTokenizer = Parameter("tokenizer", typ=TTFTextTokenizer, doc="")

PTFTextTokenizerWithOffsets = Parameter(
    "tokenizer", typ=TTFTextTokenizerWithOffsets, doc=""
)

PTF2Tokenizer = Parameter("tokenizer", typ=TTF2Tokenizer, doc="")

PBlackboxTokenizer = Parameter("tokenizer", typ=TBlackboxTokenizer, doc="")

PTokenizer = Parameter(
    "tokenizer",
    typ=Union(TTokenizerHugs, TTF2Tokenizer, TBlackboxTokenizer),
    doc="A Tokenizer."
)
"""
# TODO: move to testing
assert issubclass(transformers.models.albert.modeling_albert.AlbertForSequenceClassification, PModelHugsClassifier) == True
assert issubclass(transformers.models.albert.modeling_albert.AlbertForSequenceClassification, PModelHugsAudioClassifier) == False
assert issubclass(transformers.models.albert.modeling_albert.AlbertForSequenceClassification, PModelHugsTextClassifier) == True
assert issubclass(transformers.models.albert.modeling_albert.AlbertForSequenceClassification, PModel) == True
assert issubclass(transformers.models.albert.modeling_albert.AlbertForSequenceClassification, PModelTorch) == True
assert issubclass(transformers.models.albert.modeling_albert.AlbertForSequenceClassification, PModelTF1) == False
"""

# Huggingface text classifiers in the pytorch api
PModelTorchHugsTextClassifier = Parameter(
    "model", typ=Intersection(TTorchModel, PModelHugsTextClassifier), doc=""
)

# Huggingface text classifiers in the tensorflow api
PModelTFHugsTextClassifier = Parameter(
    "model", typ=Intersection(TTF2Model, PModelHugsTextClassifier), doc=""
)

PModelName = Parameter(
    "model_name", doc="The model name for a managed truera workspace.", typ=str
)

PHugsModelName = Parameter(
    "huggingface_model_name", doc="The name of a huggingface model.", typ=str
)

PProjectName = Parameter(
    "project_name", doc="Project name for managed truera workspace.", typ=str
)

PDataSplitName = Parameter(
    "data_split_name",
    doc="Data split name for managed truera workspace.",
    typ=str
)

PDataCollectionName = Parameter(
    "data_collection_name",
    doc="Data collection name for managed truera workspace.",
    typ=str
)


# Here only for its signature:
def example_get_model(path: Path) -> PModel:
    ...


PGetModel = Parameter(
    "get_model",
    doc=(
        "Function to retrieve model given a path. "
        "TODO: More details here."
    ),
    typ=Function(inspect.signature(example_get_model))
)


# Here only for its signature:
def example_eval_model(
    model: PModel, args: Tuple[Any], kwargs: Dict[str, Any]
) -> Any:
    ...


PEvalModel = Parameter(
    "eval_model",
    doc="Function to evalate a model. TODO: More details here.",
    typ=Function(inspect.signature(example_eval_model))
)

PVocab = Parameter("vocab", doc="TODO: More here.", typ=Dict[str, int])

PUnkTokenId = Parameter("unk_token_id", doc="TODO: More here.", typ=int)

PPadTokenId = Parameter("pad_token_id", doc="TODO: More here.", typ=int)

PSpecialTokens = Parameter(
    "special_tokens", doc="TODO: More here.", typ=List[int]
)


# Here only for its signature:
def example_text_to_inputs(texts: Iterable[str]) -> Dict[str, Any]:
    ...


PTextToInputs = Parameter(
    "text_to_inputs",
    doc="TODO: More here.",
    typ=Function(inspect.signature(example_text_to_inputs))
)


# Here only for its signature:
def example_text_to_token_ids(
    texts: Iterable[str]
) -> Iterable[Tuple[int, int]]:
    ...


PTextToTokenIds = Parameter(
    "text_to_token_ids",
    doc="TODO: More here.",
    typ=Function(inspect.signature(example_text_to_token_ids))
)


# Here only for its signature:
def example_text_to_spans(texts: Iterable[str]) -> Iterable[NLP.Types.Span]:
    ...


PTextToSpans = Parameter(
    "text_to_spans",
    doc="TODO: More here.",
    typ=Function(inspect.signature(example_text_to_spans))
)

PNEmbeddings = Parameter(
    "n_embeddings",
    doc="The number of dimensions in a token embedding vector.",
    typ=int
)

PNTokens = Parameter(
    "n_tokens", doc="The number of tokens accepted by a model.", typ=int
)

PDataInstance = Parameter(
    "data_instance", typ=str, doc="A single text instance."
)
PLabelInstance = Parameter(
    "label_instance", typ=int, doc="A single label instance."
)

# TODO(piotrm): prevent Sequence and Iterable from matching strings.
PDataSequence = Parameter("data_sequence", typ=Sequence, doc="A sequence.")
PLabelsSequence = Parameter(
    "labels_sequence", typ=Sequence, doc="A sequence of labels."
)

# TODO(piotrm): prevent Iterable from matching Sequence
PDataIterable = Parameter("data_iterable", typ=Iterable, doc="An interable.")
PLabelsIterable = Parameter(
    "labels_iterable", typ=Iterable, doc="An interable of labels."
)

# TODO(piotrm): prevent DataFrames/Series from matching any of the above.
PDataPandas = Parameter(
    "data_pandas", typ='pandas.DataFrame', doc="Pandas DataFrame."
)
"""
# more general handling of pytorch data in progress
PDataTorchDataset = Parameter(
    "data", typ='torch.utils.data.Dataset', doc="Torch dataset."
)
PDataTorchIterableDataset = Parameter(
    "data", typ='torch.utils.data.IterableDataset', doc="Torch iterable dataset."
)
PDataTorchDataLoaderRowwise = Parameter(
    "data", typ="torch.utils.data.DataLoader", doc="Torch data loader with a row-iterating dataset of map rows; i.e. DataLoader([dict(text='first input', label=0), ...])."
)
"""

PDataTorchColumnwise = Parameter(
    "data_torch_columnwise",
    typ=Mapping,
    doc=
    "Torch data with columns as a mapping; i.e. DataLoader(dict(text=['first input', 'second input'], label=[0, 1]))."
)
PDataTorchDataLoader = Parameter(
    "data_torch_dataloader",
    typ="torch.utils.data.DataLoader",
    doc="Torch data loader."
)

TData = Union(str, Sequence, Iterable, 'pandas.DataFrame')
TLabels = Union(int, Sequence, Iterable, 'pandas.DataFrame')

PData = Parameter("data", typ=TData, doc="A data source.")
PLabels = Parameter("label", typ=TLabels, doc="A labels source.")

PFieldText = Parameter(
    "field_text", str, "Name of the text field in a data source."
)
PFieldLabel = Parameter(
    "field_label", str, "Name of the label field in a data source."
)


# Here only for its signature:
def example_ds_from_source(data_path: Path) -> Iterable[Any]:
    ...


PDSFromSource = Parameter(
    "ds_from_source",
    doc="TODO: More here.",
    typ=Function(inspect.signature(example_ds_from_source))
)


# Here only for its signature:
def example_standardize_databatch(databatch: Any) -> Dict[str, Any]:
    ...


PStandardizeDatabatch = Parameter(
    "standardize_databatch",
    doc="TODO: More here.",
    typ=Function(inspect.signature(example_standardize_databatch))
)

PEmbeddingLayer = Parameter(
    "embedding_layer",
    doc=(
        "The model layer where token embeddings are computed. "
        "See Also `PEmbeddingAnchor`."
    ),
    typ=str
)

PEmbeddingAnchor = Parameter(
    "embedding_anchor", doc="TODO: More here.", typ=LayerAnchor
)

POutputLayer = Parameter(
    "output_layer",
    doc=(
        "The model layer from which a quantity of interest is defined. "
        "See also `POutputAnchor`."
    ),
    typ=str
)

POutputAnchor = Parameter(
    "output_anchor", doc="TODO: More here.", typ=LayerAnchor
)

PNOutputNeurons = Parameter(
    "n_output_neurons", doc="Number of neurons in the output layer.", typ=int
)

PNRecords = Parameter(
    "n_records", doc="INTERNAL USE ONLY: data length", typ=int
)

PNMetricsRecords = Parameter(
    "n_metrics_records", doc="TODO: More here.", typ=int
)

PRefToken = Parameter("ref_token", doc="TODO: More here.", typ=str)

PUseTrainingMode = Parameter(
    "use_training_mode",
    doc="Use training mode when computing gradients.",
    typ=bool
)

PResolution = Parameter(
    "resolution",
    doc=(
        "Baseline-to-instance interpolation resolution. "
        "Higher produces more accurate influences."
    ),
    typ=int
)

PRebatchSize = Parameter(
    "rebatch_size",
    doc=(
        "The number of instances to send to a model at once. "
        "May result in out-of-memory error if set too large."
    ),
    typ=int
)

PScoreType = Parameter("score_type", doc="Model score type.", typ=str)

PClassificationThreshold = Parameter(
    "classification_threshold",
    doc="Threshold for binary classifiers.",
    typ=float
)

PTrulensWrapper = Parameter("trulens_wrapper", doc="TODO: More here.", typ=str)

# Parameters used in debugging/demos.
PDebugModel = Parameter("debug_model", doc="", typ=str)
PDebugArg = Parameter("debug_arg", doc="", typ=int)
PDebugInfer = Parameter("debug_infer", doc="", typ=int)
