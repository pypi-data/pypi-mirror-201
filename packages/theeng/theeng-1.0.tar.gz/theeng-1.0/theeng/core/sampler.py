from collections import defaultdict
from typing import Callable, Dict, List, Tuple

from numpy import concatenate
from pandas import DataFrame
from scipy.stats import qmc

from theeng.algorithms.samplers import Samplers
from theeng.core.abstract import Step
from theeng.core.problem import ProblemConstructor


class Sampler(Step):
    def __init__(
        self,
        problem: ProblemConstructor,
        evaluator: Callable[[Dict[str, float]], Dict[str, float]],
    ) -> None:
        super().__init__(problem, evaluator)

    def sample(
        self, samplerName: str = "latinHypercube", nSamples: int = 50
    ) -> Tuple[List[List[float]], List[List[float]], DataFrame]:
        problem = SamplingProblem(self.problem, self.evaluator)
        samplerMethod = self._getMethod(Samplers, samplerName, nVar=self.nVar)()

        samp = samplerMethod.random(n=nSamples)
        x = qmc.scale(samp, self.lowerBounds, self.upperBounds).tolist()

        out = defaultdict(list)
        res = problem._evaluate(x, out)  # type: ignore

        f = res["F"]
        r = res["R"]

        data = concatenate([x, r], axis=1)
        data = DataFrame(
            data,
            columns=self.pNames
            + self.resultsExpressions
            + self.objectiveExpressions
            + self.constraintExpressions,
        )

        data = data.T.drop_duplicates().T

        return x, f, data


class SamplingProblem:
    def __init__(
        self,
        problem: ProblemConstructor,
        evaluator: Callable[[Dict[str, float]], Dict[str, float]],
    ):
        """Initialize the sampling problem.

        Args:
            problem (ProblemConstructor): The problem to be evaluated.
            evaluator (Evaluator): The evaluator to be used.
        """
        self._evaluator = evaluator

        self._nVar = problem.getNvar()
        self._pNames = problem.getPnames()

        self._objectives = problem.getObjectives()
        self._constraints = problem.getConstraints()
        self._lowerBounds, self._upperBounds = problem.getBounds()

    def _evaluate(
        self, x: List[List[float]], out: Dict[str, List[List[float]]], *args, **kwargs
    ) -> Dict[str, List[List[float]]]:
        """Evaluate the sampling problem on the given samples.

        Args:
            x (List[List[float]]): Parameters samples.
            out (Dict[str, List[List[float]]]): Retruned dictionary (inspired by Pymoo).

        Returns:
            Dict[str, List[List[float]]]: The evaluated samples, objectives and constraints.
        """
        f = []
        g = []
        r = []

        for sample in x:
            parameters = {name: value for name, value in zip(self._pNames, sample)}
            results = self._evaluator(parameters)

            objs = [obj(results) for obj in self._objectives]
            consts = [constr(results) for constr in self._constraints]
            res = list(results.values()) + objs + consts

            f.append(objs)
            g.append(consts)
            r.append(res)

        out["F"] = f
        out["G"] = g
        out["R"] = r

        return out
