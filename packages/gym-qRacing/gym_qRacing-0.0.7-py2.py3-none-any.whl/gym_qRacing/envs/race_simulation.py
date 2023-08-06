import gym
from gym import spaces
import numpy as np
import json

from .classes import AgentCar, Participant
from .functions import Helper, Logging
from .models import model_startingGrid, model_lap


class RaceSimulation(gym.Env):
    def __init__(self, config): # the passed "config" parameter is defined in the initialization of the environment (eg. notebook)
        #* Global config
        self.config = config
        self.info = {}

        #* Observation space (from config .yaml)
        self.low = np.array([config['QLEARNING']['ENV_OBSERVATION_LOW'][0], config['QLEARNING']['ENV_OBSERVATION_LOW'][1]], dtype=np.int)
        self.high = np.array([config['QLEARNING']['ENV_OBSERVATION_HIGH'][0], config['QLEARNING']['ENV_OBSERVATION_HIGH'][1]], dtype=np.int)
        self.observation_space = spaces.Box(self.low, self.high, dtype=np.int)
        
        #* Action space
        self.action_space = spaces.Discrete(4)

        #* Agent car
        self.agent_car = AgentCar(Participant(
            "Agent", # participant_id
            config['RACESIMULATION']['RACE_INITFUELMASS'], # init fuel mass
            0, # this is overridden when initializing the actual race_grid!
        ))

        #* (Lap) Models
        self.model_lap = model_lap(config)

        #* Static parameters for the race simulation
        self.race_length = config['RACESIMULATION']['RACE_LENGTH'] # length of the race
        self.race_gridSize = config['RACESIMULATION']['RACE_GRIDSIZE'] # amount of participants
        self.race_lap = 1 # current lap of the race
        self.race_grid = [] # array of participant instances



    #
    # * this function (re)initializes the simulation. 
    #
    def reset(self, seed=None, options={}):
        # logging
        Helper.global_logging(self.config['LOGGING'], "ENVIRONMENT", "\n[bold red]Initializing simulation...[/bold red]\n")
        

        # * resetting simulation
        self.race_length = self.config['RACESIMULATION']['RACE_LENGTH'] # length of the race
        self.race_gridSize = self.config['RACESIMULATION']['RACE_GRIDSIZE'] # amount of participants
        self.race_lap = 1 # current lap of the race
        self.race_grid = [] # array of participant instances
        self.model_lap = model_lap(self.config)
        self.agent_car = AgentCar(Participant(
            "Agent", # participant_id
            self.config['RACESIMULATION']['RACE_INITFUELMASS'], # init fuel mass
            0, # this is overridden when initializing the actual race_grid!
        ))


        # * generating starting grid
        self.race_grid = model_startingGrid.gen_startingGrid(self.config, self.agent_car, self.race_gridSize)

        # logging starting grid
        if self.config['LOGGING']['SIMULATION']['GRID_GENERATION']:
            Logging.log_starting_grid(self.race_lap, self.race_grid)


        # * generating accidents and code60 phases
        # TODO: implement generating accidents and code60 phases
        # ! this is not done yet!!!


        # * generating and returning initial observation
        obs = self.observe()
        return obs, self.info


    #
    # * this function simulates each time step
    #
    def step(self, action):       
        # * 1 - perform the action chosen by the agent
        agent_action = self.agent_car.take_action(action, self.race_lap)

        # * 2 - simulating laps for all participants      
        self.model_lap.simulate_lap(self.race_lap, self.race_grid)

        # * 3 - Generate required return values
        obs = self.observe() # getting current state of environment
        reward = self.agent_car.calc_reward() # calculating reward based on last action

        # * 4 - checking if episode is terminal
        done = self.is_done() 

        # creating info dict 
        info = {
            "done": done,
            "race_lap": self.race_lap,
            "agent": {
                "action": action,
                "reward": reward,
                "position": self.agent_car.car.race_position,
                "pitStop_cnt": len(self.agent_car.car.car_pitStops),
                "current_tireDeg": self.agent_car.car.car_tireDeg,
                "current_fuelMass": self.agent_car.car.car_fuelMass
            },
            "observation": obs,
            "participant_log": self.agent_car.car.log,
            # TODO: add "grid" field containing all participant.log values!
        }

        # saving to global variable
        self.info = info


        # logging
        Helper.global_logging(self.config['LOGGING']['SIMULATION'], "LAP", "\nSimulating Lap [bold]#{}[/bold]".format(self.race_lap))
        Helper.global_logging(self.config['LOGGING']['AGENT'], "ACTIONS", "[yellow]Agent took action {}, got {} in reward and moved {} positions[/yellow]\n".format(agent_action, reward, (self.agent_car.car.lastLap_position - self.agent_car.car.race_position) ))
        if self.config['LOGGING']['SIMULATION']['GRID_POSITIONS']: # logging table of all participant timings for this lap
            Logging.log_lap_timings(self.race_lap, self.race_grid)

        # increasing lap count
        self.race_lap += 1

        # * returning required fields for this step
        return obs, reward, done, info


    #
    # * this function creates the observation object for the agent
    #
    def observe(self):
        # * read and return observation (defined in config.yaml)
        
        observation = (
            int(getattr(self.agent_car.car, self.config['QLEARNING']['ENV_OBSERVATION_FIELDS'][0])), 
            int(getattr(self.agent_car.car, self.config['QLEARNING']['ENV_OBSERVATION_FIELDS'][1]))
        )

        return observation


    #
    # * this function checks if a terminal state is achieved
    #
    def is_done(self):
        # * check if all laps have been simulated
        if self.race_lap > self.race_length or self.agent_car.car.is_retired:
            Helper.global_logging(self.config['LOGGING']['SIMULATION'], "DONE", "[bold red]Simulation finished after {} lap(s)[/bold red]".format(self.race_lap-1))

            # if enabled, dump JSON logs after each episode
            if self.config['LOGGING']['DUMP']:
                for idx_sector, participant in enumerate(self.race_grid):
                    with open('./logs/'+participant.participant_id+'.json', 'w') as fout:
                        json.dump(participant.log, fout)
            return True
        
        # * otherwise, keep simulating the race
        else:
            return False


    #
    # * this function is mandatory, but not used
    #
    def render(self, mode):
        return None