from __future__ import annotations

import re
from typing import Literal, Annotated, Union

from pydantic import Field

from src.UQpyDTO import UQpyDTO


class StretchDto(UQpyDTO):
    method: Literal['Stretch'] = 'Stretch'
    loglikelihood_file: str = Field(..., alias='logLikelihoodFile')
    loglikelihood_function: str = Field(..., alias='logLikelihoodPath')
    burn_length: int = Field(..., alias='burn-in')
    jump: int
    method: str
    dimension: int
    n_chains: int = Field(..., alias='numChains')
    random_state: int = Field(..., alias='randomState')
    scale: float

    def init_to_text(self):
        from UQpy.sampling.mcmc.Stretch import Stretch
        c = Stretch

        class_name = c.__module__.split(".")[-1]
        import_statement = "from " + c.__module__ + " import " + class_name + "\n"

        stretch_parameters = self.dict()
        stretch_parameters.pop("method")
        # likelihood_file = stretch_parameters["loglikelihood_file"]
        stretch_parameters.pop("loglikelihood_file")
        # likelihood_function = stretch_parameters["loglikelihood_function"]
        stretch_parameters.pop("loglikelihood_function")
        #
        # likelihood_filename = re.split(r'[/.]', likelihood_file)[-2]
        # import_likehood_statement = "from importlib.machinery import SourceFileLoader\n"
        # import_likehood_statement += f"log_pdf_file = SourceFileLoader('{likelihood_filename}','{likelihood_file}').load_module()\n"

        # stretch_parameters["log_pdf_target"] = f"log_pdf_file.{likelihood_function}"
        stretch_parameters["log_pdf_target"] = f"dist.log_pdf"
        str_parameters = str()
        for key in stretch_parameters:
            if stretch_parameters[key] is None: continue
            str_parameters += key + "=" + str(stretch_parameters[key]) + ","

        # prerequisite_str = import_statement + import_likehood_statement
        prerequisite_str = import_statement
        prerequisite_str += "sampling = " + class_name + "(" + str_parameters + ")\n"
        sampling_str = "sampling"

        return (prerequisite_str, sampling_str)


class MetropolisHastingsDTO(UQpyDTO):
    method: Literal['MH'] = 'MH'
    loglikelihood_file: str = Field(..., alias='logLikelihoodFile')
    loglikelihood_function: str = Field(..., alias='logLikelihoodPath')
    burn_length: int = Field(..., alias='burn-in')
    jump: int
    method: str
    dimension: int
    n_chains: int = Field(..., alias='randomState')
    random_state: int = Field(..., alias='randomState')
    scale: float


SamplingMethod = Annotated[Union[StretchDto, MetropolisHastingsDTO], Field(discriminator='method')]