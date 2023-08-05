import nemo.collections.asr as nemo_asr
import torch

asr_model = nemo_asr.models.ASRModel.from_pretrained(
    model_name="stt_en_conformer_ctc_small", map_location=torch.device("cuda")
)
asr_model.half()
asr_model.preprocessor = EncDecCTCModel.from_config_dict(asr_model._cfg.preprocessor)


asr_model.preprocessor.featurizer.dither = 0.0
asr_model.preprocessor.featurizer.pad_to = 0
asr_model.eval()
asr_model.encoder.freeze()
asr_model.decoder.freeze()

length = 16_000 * 2
input_signal = torch.randn((1, length), dtype=torch.float16)
input_signal_length = torch.tensor([length], dtype=torch.int64)

_ = asr_model.forward(input_signal=input_signal, input_signal_length=input_signal_length)
