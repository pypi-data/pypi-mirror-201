from pathlib import Path

from pydantic import BaseModel, Field
from typing import Literal, Union
from typing_extensions import Annotated

from src.UQpyDTO import UQpyDTO
from src.sampling.mcmc.StretchDto import StretchDto, SamplingMethod


class ReliabilityMethodBaseDTO(UQpyDTO):
    pass


class SubsetSimulationDTO(ReliabilityMethodBaseDTO):
    method: Literal['SubsetSimulation'] = 'SubsetSimulation'
    conditionalProbability: float
    failure_threshold: float = Field(..., alias="failureThreshold")
    maxLevels: int
    initial_samples: int
    samplingMethod: StretchDto

    def init_to_text(self):
        from UQpy.reliability.SubsetSimulation import SubsetSimulation
        from UQpy.sampling.MonteCarloSampling import MonteCarloSampling
        c = SubsetSimulation

        self.__create_postprocess_script()
        output_script = Path('postprocess_script.py')

        class_name = c.__module__.split(".")[-1]
        import_statement = "from " + c.__module__ + " import " + class_name + "\n"

        import_statement += "from " + MonteCarloSampling.__module__ + " import " + \
                            MonteCarloSampling.__module__.split(".")[-1] + "\n"

        import_statement += f"monte_carlo = {MonteCarloSampling.__module__.split('.')[-1]}(distributions=dist, nsamples={self.initial_samples})\n"
        input_str = "subset"
        initializer = f'{input_str} = {class_name}(sampling={self.samplingMethod}, ' \
                      f'conditional_probability={self.conditionalProbability}, ' \
                      f'max_level={self.maxLevels}, runmodel_object=run_model,' \
                      f'samples_init=monte_carlo.samples)\n'

        prerequisite_str = import_statement + initializer
        return prerequisite_str, input_str

    def __create_postprocess_script(self, results_filename: str = 'results.out'):
        postprocess_script_code = [
            'def compute_limit_state(index: int) -> float:',
            f"\twith open('{results_filename}', 'r') as f:",
            '\t\tres = f.read().strip()',
            '\tif res:',
            '\t\ttry:',
            '\t\t\tres = float(res)',
            '\t\texcept ValueError:',
            "\t\t\traise ValueError(f'Result should be a single float value, check results.out file for sample evaluation {index}')",
            '\t\texcept Exception:',
            '\t\t\traise',
            '\t\telse:',
            f"\t\t\treturn {self.failure_threshold} - res",
            '\telse:',
            "\t\traise ValueError(f'Result not found in results.out file for sample evaluation "
            + "{index}')",
        ]

        with open("postprocess_script.py", "w") as f:
            f.write("\n".join(postprocess_script_code))


class FormDTO(ReliabilityMethodBaseDTO):
    method: Literal['FORM'] = 'FORM'


ReliabilityMethod = Annotated[Union[SubsetSimulationDTO, FormDTO], Field(discriminator='method')]
