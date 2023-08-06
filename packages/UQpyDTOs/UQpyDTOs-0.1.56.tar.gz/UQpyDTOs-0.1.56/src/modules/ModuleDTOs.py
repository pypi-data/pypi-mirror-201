from pydantic import BaseModel, Field
from typing import Literal, Union
from typing_extensions import Annotated
from src.reliability.ReliabilityMethodsDTOs import ReliabilityMethod


class ModuleBaseDTO(BaseModel):
    pass


class SamplingDTO(ModuleBaseDTO):
    uqType: Literal['Sampling'] = 'Sampling'

    def generate_code(self):
        pass

class SurrogatesDTO(ModuleBaseDTO):
    uqType: Literal['Surrogates'] = 'Surrogates'

class ReliabilityDTO(ModuleBaseDTO):
    uqType: Literal['Reliability'] = 'Reliability'
    methodData: ReliabilityMethod


ModuleDTO = Annotated[Union[ReliabilityDTO, SamplingDTO], Field(discriminator='uqType')]
