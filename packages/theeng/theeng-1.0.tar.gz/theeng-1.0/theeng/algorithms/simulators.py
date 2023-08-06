from collections import defaultdict
from json import load
from os.path import exists
from sys import path
from typing import Dict, Iterable, List, Union

from numpy import average, max, min

f = open("configs\\settings.json")
data = load(f)
freeCADBinPath = data["FREECAD_PATH"]
if not exists(freeCADBinPath):
    raise FileNotFoundError(
        "provided FreeCAD binary directory does not exists. Check FreeCAD installation path in settings.json file."
    )

path.append(data["FREECAD_PATH"])

import FreeCAD
from femtools import ccxtools


class Simulators:
    def __init__(
        self,
        resultsExpressions: List[str],
        iterableOutput: List[Union[str, None]],
        fcdPath: str,
    ) -> None:
        """Initialize an FEM evaluator.

        Args:
            problem (ProblemConstructor): problem to be evaluated.
            resultsRequest (List[str]): list of results aliases contained in the spreadsheet.
            fcdPath (str): path to the FreeCAD file containing the model.
        """
        self.resultsExpressions = resultsExpressions
        self.iterableOutput = iterableOutput
        self._doc = FreeCAD.open(fcdPath)
        self._sheet = self._doc.getObject("Spreadsheet")

    def femSimulator(self, parameters: Dict[str, float]) -> Dict[str, float]:
        """Evaluate the design parameters and return the results by updating the spreadsheet and running the FEM analysis in FreeCAD.

        Args:
            parameters (Dict[str, float]): dictionary of design parameters containing aliases and values contained in the spreadsheet.

        Returns:
            Dict[str, float]: dictionary containing results aliases and values.
        """

        for key, value in parameters.items():
            self._sheet.set(key, str(value))

        # self._sheet.recompute()
        self._doc.recompute()

        fea = ccxtools.FemToolsCcx()
        fea.update_objects()
        fea.setup_working_dir()
        fea.setup_ccx()
        message = fea.check_prerequisites()
        if not message:
            fea.purge_results()
            fea.write_inp_file()
            fea.ccx_run()
            fea.load_results()
        else:
            print(
                "Houston, we have a problem! {}\n".format(message)
            )  # in Python console

        self._sheet.recompute()
        results = defaultdict(float)
        for result, iterableAction in zip(self.resultsExpressions, self.iterableOutput):
            if result in parameters:
                ccx_result = parameters[result]
            else:
                ccx_result = self._sheet.get(result)
            if iterableAction is None:
                if not isinstance(ccx_result, float):
                    raise Exception("Result is not float.")
                results[result] = ccx_result
            elif iterableAction == "Max":
                if not isinstance(ccx_result, Iterable):
                    raise Exception("Result is not Iterable.")
                results[result] = max(ccx_result)  # type: ignore
            elif iterableAction == "Min":
                if not isinstance(ccx_result, Iterable):
                    raise Exception("Result is not Iterable.")
                results[result] = min(ccx_result)  # type: ignore
            elif iterableAction == "Avg":
                if not isinstance(ccx_result, Iterable):
                    raise Exception("Result is not Iterable.")
                results[result] = average(ccx_result)  # type: ignore
            else:
                raise Exception("Invalid iterable action.")

        return results

    def cfdSimulator(self, parameters: Dict[str, float]) -> Dict[str, float]:
        raise NotImplementedError("CFD interface is not implemented yet.")
