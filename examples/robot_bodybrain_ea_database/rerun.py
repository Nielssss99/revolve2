"""Rerun the best robot between all experiments."""

import logging

import config
from evaluator import Evaluator
import os
os.environ['ALGORITHM'] = config.ALGORITHM

if os.environ["Algorithm"] == "CPPN":
    from genotype import Genotype
elif os.environ["Algorithm"] == "GRN":
    from genotype_grn import Genotype
from individual import Individual
from sqlalchemy import select
from sqlalchemy.orm import Session

from revolve2.experimentation.database import OpenMethod, open_database_sqlite
from revolve2.experimentation.logging import setup_logging


def main() -> None:
    """Perform the rerun."""
    setup_logging()

    # Load the best individual from the database.
    dbengine = open_database_sqlite(
        config.DATABASE_FILE, open_method=OpenMethod.OPEN_IF_EXISTS
    )

    with Session(dbengine) as ses:
        rows = ses.execute(
            select(Genotype, Individual.fitness)
            .join_from(Genotype, Individual, Genotype.id == Individual.genotype_id)
            .order_by(Individual.fitness.desc()).limit(50)
        ).fetchall() #.one()
        #assert row is not None
        
    for row in rows[0:]:
        genotype = row[0]
        fitness = row[1]

        if os.environ["Algorithm"] == "CPPN":
            modular_robot = genotype.develop(zdirection = config.ZDIRECTION, include_bias = config.CPPNBIAS,
                include_chain_length = config.CPPNCHAINLENGTH, include_empty = config.CPPNEMPTY,
                max_parts = config.MAX_PARTS, mode_collision = config.MODE_COLLISION,
                mode_core_mult = config.MODE_CORE_MULT, mode_slots4face = config.MODE_SLOTS4FACE,
                mode_slots4face_all = config.MODE_SLOTS4FACE_ALL, mode_not_vertical = config.MODE_NOT_VERTICAL)
        elif os.environ["Algorithm"] == "GRN":
            modular_robot = genotype.develop(include_bias = config.CPPNBIAS, max_parts = config.MAX_PARTS)

        logging.info(f"Best fitness: {fitness}")

        # Create the evaluator.
        evaluator = Evaluator(headless = True, num_simulators = 1, terrain = config.TERRAIN, fitness_function = config.FITNESS_FUNCTION,
                              simulation_time = config.SIMULATION_TIME, sampling_frequency = config.SAMPLING_FREQUENCY,
                              simulation_timestep = config.SIMULATION_TIMESTEP, control_frequency = config.CONTROL_FREQUENCY)

        # Show the robot.
        evaluator.evaluate([modular_robot])

        


if __name__ == "__main__":
    main()
