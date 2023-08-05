from typing import List, Union

import os
import soundfile as sf
import numpy as np

from olab.base import simple_chunker, simple_featurizer
from olab.types import WaveForm
from omodel.outliers.pystroll import OutlierModel as Stroll
from meshed import code_to_dag


def bytes_to_wf(wav_bytes: bytes) -> WaveForm:
    wf, sr = decode_wav_bytes(wav_bytes)
    # wav, sr = sf.read(wav_bytes)
    return np.array(wf)


# ML steps
def learn_model(fvs, n_centroids=5):
    model = Stroll(n_centroids=n_centroids)
    model.fit(X=fvs)

    return model


def apply_model(fvs, fitted_model):
    scores = fitted_model.score_samples(X=fvs)
    return scores


d = {
    'bytes_to_wf': bytes_to_wf,
    'simple_chunker': simple_chunker,
    'simple_featurizer': simple_featurizer,
    'learn_model': learn_model,
    'apply_model': apply_model,
}

# simple DPP in form of a DAG
@code_to_dag(func_src=d)
def simple_dpp(wav_bytes: bytes):
    wfs = bytes_to_wf(wav_bytes)
    chks = simple_chunker(wfs)
    fvs = simple_featurizer(chks)
    model = learn_model(fvs)
    scores = apply_model(fvs, model)


if __name__ == '__main__':
    # make input data for testing purposes
    from recode.audio import decode_wav_bytes
    from pyckup import grab

    f1 = grab('https://www.dropbox.com/s/yueb7mn6mo6abxh/0_0.wav?dl=0')

    wf, sr = decode_wav_bytes(f1)
    print(wf[:50])
    # wfs = upload_sound(wav_list)

    # print(type(wfs))

    # # run the experiment
    scores = simple_dpp(f1)

    print(scores)
