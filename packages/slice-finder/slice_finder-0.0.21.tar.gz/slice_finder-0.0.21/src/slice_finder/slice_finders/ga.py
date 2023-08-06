import random
from typing import Any, Callable

from deap import base, creator, tools
from deap.algorithms import varOr
import numpy as np

from slice_finder.slice_finders.slice_finder import SliceFinder
from slice_finder.types import Extreme, Filter


class GASliceFinder(SliceFinder):
    """Slice discovery using Genetic algorithm."""

    def create_individual(self, n_filters: int):
        return creator.Individual(self.data_structure.get_n_filters(n_filters))

    def mutate_individual(self, individual: list[Filter], indpb: float):
        for i in range(len(individual)):
            if random.random() < indpb:
                individual[i] = self.data_structure.get_filter()
        return (individual,)

    def eval_individual(
        self,
        individual: list[Filter],
        **kwargs,
    ):
        df = self.data_connector.filter(individual)
        if len(df) < len(self.data_connector.data) * kwargs["min_size"]:
            return None
        return (kwargs["metric"](df),)

    def eaMuPlusLambda(
        self,
        population: list[Any],
        toolbox: base.Toolbox,
        mu: int,
        lambda_: int,
        cxpb: float,
        mutpb: float,
        ngen: int,
        stats: tools.Statistics,
        halloffame: tools.HallOfFame,
        maximize: bool,
        maximum: float,
        minimum: float,
    ):
        """Modified deap.algorithms.eaMuPlusLambda."""

        logbook = tools.Logbook()
        logbook.header = ["gen", "nevals"] + (stats.fields if stats else [])
        should_stop = False

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            if fit is None:
                continue
            if (maximize and sum(fit) >= maximum) or (not maximize and sum(fit) <= minimum):
                should_stop = True
            ind.fitness.values = fit

        halloffame.update(population)

        record = stats.compile([ind for ind in population if ind.fitness.valid])
        logbook.record(gen=0, nevals=len(invalid_ind), **record)
        if self.verbose:
            print(logbook.stream)

        if should_stop:
            return population, logbook

        # Begin the generational process
        for gen in range(1, ngen + 1):
            # Vary the population
            offspring = varOr(population, toolbox, lambda_, cxpb, mutpb)

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                if fit is None:
                    continue
                if (maximize and sum(fit) >= maximum) or (not maximize and sum(fit) <= minimum):
                    should_stop = True
                ind.fitness.values = fit

            # Update the hall of fame with the generated individuals
            halloffame.update(offspring)

            # Select the next generation population
            population[:] = toolbox.select(population + offspring, mu)

            # Update the statistics with the new population
            record = stats.compile([ind for ind in population if ind.fitness.valid])
            logbook.record(gen=gen, nevals=len(invalid_ind), **record)
            if self.verbose:
                print(logbook.stream)

            if should_stop:
                return population, logbook

        return population, logbook

    def create_toolbox(
        self,
        maximize: bool,
        n_filters: int,
        metric: Callable[[Any], float],
        min_size: float,
        indpb: float,
    ):
        creator.create("FitnessMulti", base.Fitness, weights=(1.0,) if maximize else (-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMulti)

        toolbox = base.Toolbox()
        toolbox.register("individual", self.create_individual, n_filters)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", self.mutate_individual, indpb=indpb)
        toolbox.register("select", tools.selBest)
        toolbox.register(
            "evaluate",
            self.eval_individual,
            metric=metric,
            min_size=min_size,
        )

        return toolbox

    def find_extreme(
        self,
        metric: Callable[[Any], float],
        n_hof=1,
        n_generations=10,
        population_size=100,
        n_filters=3,
        maximize=False,
        min_size=0.01,
        cxpb=0.5,
        mutpb=0.5,
        indpb=0.5,
        maximum=float("inf"),
        minimum=float("-inf"),
    ) -> list[Extreme]:
        """Find slice with an extreme value of a metric.
        
        Args:
            metric: Function that calculates metric value over data
            n_hof: Number of extreme values to return
            n_generations: Number of iterations
            population_size: Population size
            n_filters: Number of filters
            maximize: `True` will search for the maximum
            metric's value, and `False` will search for the minumum one
            min_size: Minimum size, in fractions, of the extreme subset.
            For exmaple, for value `0.01`, the extreme subset must be at
            least 1% of the data, in size, to be considered
            cxpb: The probability of mating two individuals
            mutpb: The probability of mutating an individual
            indpb: The probability of mutating an individual's filter
            maximum: If `maximize`, and `maximum` is reached, the search stoppes
            minimum: If `not maximize`, and `minimum` is reached, the search stoppes
        """

        if n_filters <= 1:
            raise ValueError("n_filters must be larger than 1.")

        toolbox = self.create_toolbox(
            n_filters=n_filters,
            maximize=maximize,
            metric=metric,
            min_size=min_size,
            indpb=indpb,
        )
        pop = toolbox.population(n=population_size)
        hof = tools.HallOfFame(n_hof)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("min", np.min)
        stats.register("max", np.max)

        self.eaMuPlusLambda(
            pop,
            toolbox,
            mu=population_size,
            lambda_=population_size,
            cxpb=cxpb,
            mutpb=mutpb,
            ngen=n_generations,
            stats=stats,
            halloffame=hof,
            maximize=maximize,
            maximum=maximum,
            minimum=minimum,
        )

        return [Extreme(
            data_metric_value=metric(self.data_connector.data),
            filtered_data=self.data_connector.filter(best_filters),
            filtered_data_metric_value=best_filters.fitness.values[0],
            filters=best_filters,
        ) for best_filters in hof]
