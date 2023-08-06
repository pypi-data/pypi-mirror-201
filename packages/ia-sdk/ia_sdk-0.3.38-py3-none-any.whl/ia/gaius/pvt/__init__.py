import math
import functools
import json
import operator
from copy import deepcopy
from collections import Counter, defaultdict
from uuid import uuid4
from itertools import chain
from traceback import print_exc
import matplotlib.pyplot as plt
import pandas as pd

# Data
from sklearn.metrics import accuracy_score
import numpy as np

# Gaius Agent
from ia.gaius.agent_client import AgentClient
from ia.gaius.pvt.mongo_interface import MongoData, MongoResults
from ia.gaius.data_ops import Data
from ia.gaius.pvt.pvt_utils import retrieve_emotive_val, emotives_polarity_metrics_builder, \
    emotives_value_metrics_builder, make_modeled_emotives_, init_emotive_on_node, classification_metrics_builder, plot_confusion_matrix
from ia.gaius.prediction_models import hive_model_classification, average_emotives, prediction_ensemble_model_classification

class PVTAbortError(Exception):
    "Raised when PVT is aborted by Celery. Used to exit cleanly from nested test/train functions"

class PVTMessage():
    """Wrapper for PVT socket messages to be sent during training and testing"""
    def __init__(self, status: str,
                 current_record: int,
                 total_record_count: int,
                 metrics: dict,
                 cur_test_num: int,
                 total_test_num: int,
                 test_id: str = None,
                 user_id: str = '',
                 test_type: str = 'default'):
        self.status = status
        self.current_record = current_record
        self.total_record_count = total_record_count
        self.metrics = metrics
        self.test_id = test_id
        self.user_id = user_id
        self.cur_test_num = cur_test_num
        self.total_test_num = total_test_num
        self.test_type = test_type

    def toJSON(self):
        return {'status': self.status,
                'current_record': self.current_record,
                'total_record_count': self.total_record_count,
                'metrics': self.metrics,
                'test_id': self.test_id,
                'user_id': self.user_id,
                'cur_test_num': self.cur_test_num,
                'total_test_num': self.total_test_num,
                'test_type': self.test_type
                }


class PerformanceValidationTest():
    """
    Performance Validation Test (PVT) - Splits a GDF folder into training and testing sets.
    Based on the test type certain visualizations will be produced.

    Test types:

    - Classification
    - Emotive Value
    - Emotives Polarity
    """
    def __init__(self,
                 agent: AgentClient,
                 ingress_nodes: list,
                 query_nodes: list,
                 num_of_tests: int,
                 pct_of_ds: float,
                 pct_res_4_train: float,
                 test_type: str,
                 dataset_location: str = 'filepath',
                 results_filepath=None,
                 ds_filepath: str = None,
                 test_prediction_strategy="continuous",
                 clear_all_memory_before_training: bool = True,
                 turn_prediction_off_during_training: bool = False,
                 shuffle: bool = False,
                 sio=None,
                 task=None,
                 user_id: str = None,
                 mongo_db=None,
                 dataset_info: dict = None,
                 test_id=None,
                 test_configuration: dict = {},
                 socket_channel: str = 'pvt_status',
                 QUIET: bool = False):
        """Initialize the PVT object with all required parameters for execution

        Args:
            agent (AgentClient): GAIuS Agent to use for trainings
            ingress_nodes (list): Ingress nodes for the GAIuS Agent (see :func:`ia.gaius.agent_client.AgentClient.set_query_nodes`)
            query_nodes (list): Query nodes for the GAIuS Agent (see :func:`ia.gaius.agent_client.AgentClient.set_query_nodes`)
            num_of_tests (int): Number of test iterations to complete
            pct_of_ds (float): Percent of the dataset to use for PVT (overall)
            pct_res_4_train (float): Percent of the dataset to be reserved for training
            test_type (str): classification, emotives_value, or emotives_polarity
            dataset_location (str): Location of dataset to utilise, "mongodb", or "filepath"
            results_filepath (_type_): Where to store PVT results
            ds_filepath (str): Path to the directory containing training GDFs
            test_prediction_strategy (str, optional): _description_. Defaults to "continuous".
            clear_all_memory_before_training (bool, optional): Whether the GAIuS agent's memory should be cleared before each training. Defaults to True.
            turn_prediction_off_during_training (bool, optional): Whether predictions should be disabled during training to reduce computational load. Defaults to False.
            shuffle (bool, optional): Whether dataset should be shuffled before each test iteration. Defaults to False.
            sio (_type_, optional): SocketIO object to emit information on. Defaults to None.
            task (_type_, optional): Celery details to emit information about. Defaults to None.
            user_id (str, optional): user_id to emit information to on SocketIO. Defaults to ''.
            mongo_db (pymongo.MongoClient, optional): MongoDB where dataset should be retrieved from
            dataset_info (dict, optional): information about how to retrieve dataset, used for MongoDB query. If dataset_location is mongodb, this must have the user_id, dataset_id, results_collection, logs_collection, and data_files_collection_name keys
            test_id (str, optional): unique identifier to be sent with messages about this test. Also used for storing to mongodb
            test_configuration (dict, optional): dictionary storing additional metadata about test configuration, to be saved in mongodb with test results
            socket_channel (str, optional): SocketIO channel to broadcast results on. Defaults to 'pvt_status'
            QUIET (bool, optional): flag used to disable log output during PVT. Defaults to False
        """

        self.agent                               = agent
        self.ingress_nodes                       = ingress_nodes
        self.query_nodes                         = query_nodes
        self.num_of_tests                        = num_of_tests
        self.dataset_location                    = dataset_location
        self.ds_filepath                         = ds_filepath
        self.results_filepath                    = results_filepath
        self.pct_of_ds                           = pct_of_ds
        self.pct_res_4_train                     = pct_res_4_train
        self.shuffle                             = shuffle
        self.test_type                           = test_type
        self.clear_all_memory_before_training    = clear_all_memory_before_training
        self.turn_prediction_off_during_training = turn_prediction_off_during_training
        self.test_prediction_strategy            = test_prediction_strategy

        self.emotives_set                        = None
        self.labels_set                          = None
        self.predictions                         = None
        self.actuals                             = None
        self.emotives_metrics_data_structures    = None
        self.class_metrics_data_structures       = None
        self.metrics_dataframe                   = None
        self.pvt_results                         = None
        self.sio                                 = sio
        self.task                                = task
        self.user_id                             = user_id
        self.mongo_db                            = mongo_db
        self.dataset_info                        = dataset_info
        self.test_id                             = test_id
        self.testing_log                         = []
        self.mongo_results                       = None
        self.test_configuration                  = test_configuration
        self.labels_counter                      = Counter()
        self.socket_channel                      = socket_channel
        self.QUIET                               = QUIET

        self.agent_genes = {}

        all_nodes = [node['name'] for node in self.agent.all_nodes]
        self.agent_genes = self.agent.get_all_genes(nodes=all_nodes)
        self.test_configuration['initial_agent_genes'] = self.agent_genes
        self.test_configuration['genome'] = self.agent.genome.topology

        if dataset_location == 'mongodb':
            self.dataset = MongoData(mongo_dataset_details=self.dataset_info, data_files_collection_name=self.dataset_info['data_files_collection_name'], mongo_db=mongo_db)
            self.mongo_results = MongoResults(mongo_db=self.mongo_db, result_collection_name=self.dataset_info['results_collection'],
                                              log_collection_name=self.dataset_info['logs_collection'], test_id=self.test_id, user_id=self.user_id,
                                              dataset_id=self.dataset_info['dataset_id'], test_configuration=self.test_configuration)
        elif dataset_location == 'filepath':
            self.dataset = Data(data_directories=[self.ds_filepath])
        elif dataset_location == 'prepared':
            self.dataset = self.ds_filepath
        elif dataset_location == 'prepared_obj':
            self.dataset = self.ds_filepath

        else:
            raise Exception(f'unknown value for dataset location: {dataset_location}')

        # Show Agent status by Default
        self.agent.show_status()

        # Assign Ingress and Query Nodes
        self.agent.set_ingress_nodes(nodes=self.ingress_nodes)
        self.agent.set_query_nodes(nodes=self.query_nodes)

        # Setting summarize single to False by default in order to handle multiply nodes topologies
        self.agent.set_summarize_for_single_node(False)
        
        if not self.QUIET:
            print(f"num_of_tests      = {self.num_of_tests}")
            print(f"ds_filepath       = {self.ds_filepath}")
            print(f"pct_of_ds         = {self.pct_of_ds}")
            print(f"pct_res_4_train   = {self.pct_res_4_train}")
            print(f"summarize_for_single_node status   = {self.agent.summarize_for_single_node}")

    def prepare_datasets(self):
        if self.dataset_location == 'prepared':
            if not self.QUIET:
                print(f"Length of Training Set = {len(self.dataset.train_sequences)}\n")
                print(f"Length of Testing Set  = {len(self.dataset.test_sequences)}\n")
            return

        elif self.dataset_location == 'prepared_obj':
            if not self.QUIET:
                print(f"Length of Training Set = {len(self.dataset.train_sequences)}\n")
                print(f"Length of Testing Set  = {len(self.dataset.test_sequences)}\n")
            return
        else:
            self.dataset.prep(
                percent_of_dataset_chosen=self.pct_of_ds,
                percent_reserved_for_training=self.pct_res_4_train,
                shuffle=self.shuffle
            )
            if not self.QUIET:
                print(f"Length of Training Set = {len(self.dataset.train_sequences)}\n")
                print(f"Length of Testing Set  = {len(self.dataset.test_sequences)}\n")
        return

    def run_classification_pvt(self):
        for test_num in range(0, self.num_of_tests):
            self.test_num = test_num
            if not self.QUIET:
                print(f'Conducting Test # {test_num}')
                print('\n---------------------\n')

            self.prepare_datasets()

            if self.sio:
                self.sio.emit(self.socket_channel,
                              PVTMessage(status='training', current_record=0, total_record_count=len(self.dataset.train_sequences),
                                         metrics={}, cur_test_num=self.test_num, total_test_num=self.num_of_tests,
                                         test_id=self.test_id, user_id=self.user_id, test_type=self.test_type).toJSON(), to=self.user_id)
            try:

                self.train_agent()

                if self.pct_res_4_train == 100:
                    print(f'Complete!')
                    continue

                self.test_agent()

                for k, labels in self.labels_set.items():
                    self.labels_set[k] = set([label.rsplit('|', maxsplit=1)[-1] for label in labels])
                if not self.QUIET:
                    print('Getting Classification Metrics...')
                self.get_classification_metrics()
                if not self.QUIET:
                    print('Saving results to pvt_results...')
                self.pvt_results.append(deepcopy(self.class_metrics_data_structures))
                self.pvt_results[test_num] = deepcopy(self.update_test_results_w_hive_classification_metrics(self.pvt_results[test_num]))

            except Exception as e:
                if not self.QUIET:
                    print('error during training/testing phase of test, remediating database for failed test, then raising error')
                if self.mongo_results:
                    if not self.QUIET:
                        print('about to remediate database')
                    self.mongo_results.deleteResults()
                    if not self.QUIET:
                        print('remediated database')

                if not self.QUIET:
                    print(f'raising error {str(e)}')
                raise e

            try:
                if self.dataset_location != 'mongodb':
                    if not self.QUIET:
                        print('Plotting Results...')
                    plot_confusion_matrix(test_num=test_num, class_metrics_data_structures=self.class_metrics_data_structures)
            except Exception as e:
                if not self.QUIET:
                    print(f'error plotting results from classification pvt: {e}')
                pass

            response_dict = {'classification_counter': self.labels_counter,
                             'pvt_results': self.pvt_results}
            result_msg = PVTMessage(status='finished', current_record=0, total_record_count=0,
                                    metrics=response_dict, cur_test_num=self.test_num, total_test_num=self.num_of_tests,
                                    test_id=self.test_id, user_id=self.user_id, test_type=self.test_type).toJSON()
            if self.sio:
                self.sio.emit(self.socket_channel,
                                result_msg, to=self.user_id)

        if self.mongo_results:
            self.mongo_results.saveResults(result_msg)
        return

    def run_emotive_value_pvt(self):
        self.pvt_results = []
        for test_num in range(0, self.num_of_tests):

            if not self.QUIET:
                print(f'Conducting Test # {test_num}')
                print('\n---------------------\n')

            self.prepare_datasets()
            if self.sio:
                self.sio.emit(self.socket_channel,
                              PVTMessage(status='training', current_record=0, total_record_count=len(self.dataset.train_sequences),
                                         metrics={}, cur_test_num=self.test_num, total_test_num=self.num_of_tests,
                                         test_id=self.test_id, user_id=self.user_id, test_type=self.test_type).toJSON(), to=self.user_id)

            self.train_agent()

            if self.pct_res_4_train == 100:
                print(f'Complete!')
                return

            self.test_agent()
            
            if not self.QUIET:
                print('Getting Emotives Value Metrics...')
            self.get_emotives_value_metrics()
            if not self.QUIET:
                print('Saving results to pvt_results...')
            self.pvt_results.append(deepcopy(self.emotives_metrics_data_structures))
            self.pvt_results[test_num] = deepcopy(self.update_test_results_w_hive_emotives_value_metrics(self.pvt_results[test_num]))
            if not self.QUIET:
                print('Plotting Results...')

            # don't try to plot emotive values if we're working to save in a mongo database
            # (its probably running without a jupyter GUI)
            if self.mongo_db is None:
                self.plot_emotives_value_charts(test_num=test_num)

        # send out finished socket message
        response_dict = {'pvt_results': self.pvt_results}

        final_msg = PVTMessage(status='finished', current_record=0, total_record_count=0,
                                     metrics=response_dict, cur_test_num=self.num_of_tests, total_test_num=self.num_of_tests,
                                     test_id=self.test_id, user_id=self.user_id, test_type=self.test_type).toJSON()
        if self.sio:
            self.sio.emit(self.socket_channel,
                          final_msg, to=self.user_id)
        if self.mongo_results:
            self.mongo_results.saveResults(final_msg)
        return

    def run_emotive_polarity_pvt(self):
        self.pvt_results = []
        for test_num in range(0, self.num_of_tests):
            if not self.QUIET:
                print(f'Conducting Test # {test_num}')
                print('\n---------------------\n')
            self.prepare_datasets()

            if self.sio:
                self.sio.emit(self.socket_channel,
                              PVTMessage(status='training', current_record=0, total_record_count=len(self.dataset.train_sequences),
                                         metrics={}, cur_test_num=self.test_num, total_test_num=self.num_of_tests,
                                         test_id=self.test_id, user_id=self.user_id, test_type=self.test_type).toJSON(), to=self.user_id)

            if not self.QUIET:
                print("Training Agent...")
            self.train_agent()

            if self.pct_res_4_train == 100:
                print(f'Complete!')
                return

            if not self.QUIET:
                print("Testing Agent...")
            self.test_agent()

            if not self.QUIET:
                print('Getting Emotives Polarity Metrics...')
            if not self.QUIET:
                print('Saving results to pvt_results...')
            self.pvt_results.append(deepcopy(self.get_emotives_polarity_metrics()))

        # send out finished socket message
        response_dict = {'pvt_results': self.pvt_results}
        final_msg = PVTMessage(status='finished', current_record=0, total_record_count=0,
                                     metrics=response_dict, cur_test_num=self.num_of_tests, total_test_num=self.num_of_tests,
                                     test_id=self.test_id, user_id=self.user_id, test_type=self.test_type).toJSON()
        if self.sio:
            self.sio.emit(self.socket_channel,
                          final_msg, to=self.user_id)
        if self.mongo_results:
            self.mongo_results.saveResults(final_msg)
        return

    def conduct_pvt(self):
        """
        Function called to execute the PVT session. Determines test to run based on 'test_type' attribute

        Results from PVT is stored in the 'pvt_results' attribute

        .. note::

            A complete example is shown in the :func:`__init__` function above. Please see that documentation for further information about how to conduct a PVT test

        """
        try:
            self.test_num = 0
            self.pvt_results = []
            self.testing_log = []

            # Validate Test Type
            if self.test_type == 'classification':
                if not self.QUIET:
                    print("Conducting Classification PVT...\n")
                self.run_classification_pvt()

            elif self.test_type == 'emotives_value':
                if not self.QUIET:
                    print("Conducting Emotives Value PVT...\n")
                self.run_emotive_value_pvt()

            elif self.test_type == 'emotives_polarity':
                if not self.QUIET:
                    print("Conducting Emotives Polarity PVT...\n")
                self.run_emotive_polarity_pvt()

            else:
                raise Exception(
                    """
                    Please choose one of the test type:
                    - classification
                    - emotives_value
                    - emotives_polarity

                    ex.
                    --> pvt.test_type='emotives_value'
                    then, retry
                    --> pvt.conduct_pvt()
                    """
                )
        # except PVTAbortError as e:
        #     print(f'Aborting PVT: {str(e)}')
        #     return
        except Exception as e:
            if not self.QUIET:
                print('\n--------------------------------------------------------------\n')
                print(f'failed to conduct PVT test, test_type={self.test_type}: {str(e)}')
                print_exc()
                print('\n--------------------------------------------------------------\n')
            raise e

    def train_agent(self):
        """
        Takes a training set of gdf files, and then trains an agent on those records.
        The user can turn prediction off if the topology doesn't have abstractions
        where prediction is needed to propagate data through the topology.
        """
        # Initialize
        if self.clear_all_memory_before_training is True:
            if not self.QUIET:
                print('Clearing memory of selected ingress nodes...')
            self.agent.clear_all_memory(nodes=self.ingress_nodes)

        if self.test_type == 'classification':
            # Start an Labels Tracker for each node
            if not self.QUIET:
                print('Initialize labels set...')
            self.labels_set = {}
            for node in self.ingress_nodes:
                self.labels_set[node] = set()
            if not self.QUIET:
                print(self.labels_set)
            self.labels_counter.clear()
            if not self.QUIET:
                print('Created labels set...')
        elif self.test_type == 'emotives_value' or self.test_type == 'emotives_polarity':
            # Start an Emotives Tracker for each node
            if not self.QUIET:
                print('Initialize emotives set...')
            self.emotives_set = {}
            for node in self.ingress_nodes:
                self.emotives_set[node] = set()
            if not self.QUIET:
                print(self.emotives_set)
                print('Created emotives set...')
        else:
            raise Exception(f"Invalid test type {self.test_type}")
        # Train Agent
        if self.turn_prediction_off_during_training is True:
            self.agent.stop_predicting(nodes=self.query_nodes)
        else:
            self.agent.start_predicting(nodes=self.query_nodes)
        if not self.QUIET:
            print('Preparing to train agent...')
        # for i, file_path in enumerate(log_progress(dataset.train_sequences)):

        train_seq_len = len(self.dataset.train_sequences)

        train_metrics = {}
        if self.test_type == 'classification':
            train_metrics = {'classification_counter': self.labels_counter}

        for j, _ in enumerate(self.dataset.train_sequences):

            training_msg = PVTMessage(status='training', current_record=j + 1, total_record_count=train_seq_len,
                                      metrics=train_metrics, cur_test_num=self.test_num, total_test_num=self.num_of_tests,
                                      test_id=self.test_id, user_id=self.user_id, test_type=self.test_type)

            self.store_train_record(test_num=self.test_num, record=training_msg)

            if j % 10 == 0:
                if self.task:
                    if self.task.is_aborted():
                        self.abort_test_remediation(current_record=j, record_count=train_seq_len)
                        return


            if j % 100 == 0:
                if not self.QUIET:
                    print(f"train - {j}")
            if self.dataset_location == 'filepath':
                with open(self.dataset.train_sequences[j], "r") as sequence_file:
                    sequence = sequence_file.readlines()
                    sequence = [json.loads(d) for d in sequence]
            elif self.dataset_location == 'prepared':
                with open(self.dataset.train_sequences[j], "r") as sequence_file:
                    sequence = sequence_file.readlines()
                    sequence = [json.loads(d) for d in sequence]
            elif self.dataset_location == 'prepared_obj':
                sequence = self.dataset.train_sequences[j]
            elif self.dataset_location == 'mongodb':
                sequence = self.dataset.getSequence(self.dataset.train_sequences[j])
            else:
                raise Exception(f"dataset location {self.dataset_location} is unknown")

            for event in sequence:
                self.agent.observe(data=event, nodes=self.ingress_nodes)
                if self.test_type == 'emotives_value' or self.test_type == 'emotives_polarity':
                    for node in self.ingress_nodes:
                        percept_emotives = list(self.agent.get_percept_data()[node]['emotives'].keys())
                        # print(f'updating emotive set for {node} with {percept_emotives}')
                        self.emotives_set[node].update(percept_emotives)
            if self.test_type == 'classification':
                for node in self.ingress_nodes:
                    self.labels_set[node].update(sequence[-1]['strings'])
                self.labels_counter.update([label.rsplit('|', maxsplit=1)[-1] for label in sequence[-1]['strings']])
            self.agent.learn(nodes=self.ingress_nodes)
        if not self.QUIET:
            print('Finished training agent!')

    def test_agent(self):
        """
        Test agent on dataset test sequences provided in self.dataset.test_sequences
        """
        # Start Testing
        self.agent.start_predicting(nodes=self.query_nodes)
        self.predictions = []
        self.actuals     = []

        self.testing_log.append([])
        test_step_info = {}
        test_seq_len = len(self.dataset.test_sequences)
        if test_seq_len == 0:
            if not self.QUIET:
                print('length of testing sequences is 0... returning\n')
            return
        for k, _ in enumerate(self.dataset.test_sequences):

            if k % 10 == 0:
                if self.task:
                    if self.task.is_aborted():
                        self.abort_test_remediation(current_record=k, record_count=test_seq_len)
                        return

            if k % 100 == 0:
                if not self.QUIET:
                    print(f"test - {k}")
            if self.dataset_location == 'filepath':
                with open(self.dataset.test_sequences[k], "r") as sequence_file:
                    sequence = sequence_file.readlines()
                    sequence = [json.loads(d) for d in sequence]
            elif self.dataset_location == 'prepared':
                with open(self.dataset.test_sequences[k], "r") as sequence_file:
                    sequence = sequence_file.readlines()
                    sequence = [json.loads(d) for d in sequence]
            elif self.dataset_location == 'prepared_obj':
                sequence = self.dataset.test_sequences[k]
            elif self.dataset_location == 'mongodb':
                sequence = self.dataset.getSequence(self.dataset.test_sequences[k])
            else:
                raise Exception(f"dataset location {self.dataset_location} is unknown")

            self.agent.clear_wm(nodes=self.ingress_nodes)
            if self.test_type == 'classification':
                # observe up to last event, which has the answer
                if len(sequence) > 2:
                    self.agent.stop_predicting(nodes=self.ingress_nodes)
                    for event in sequence[:-2]:
                        self.agent.observe(data=event, nodes=self.ingress_nodes)
                    self.agent.start_predicting(nodes=self.ingress_nodes)
                    self.agent.observe(data=sequence[-2], nodes=self.ingress_nodes)
                else:
                    for event in sequence[:-1]:
                        self.agent.observe(data=event, nodes=self.ingress_nodes)
                # get and store predictions after observing events
                self.predictions.append(self.agent.get_predictions(nodes=self.query_nodes))
                # store answers in a separate list for evaluation
                classifications_split = [label.rsplit('|', maxsplit=1)[-1] for label in sequence[-1]['strings']]
                self.actuals.append(deepcopy(classifications_split))
                for node in self.ingress_nodes:
                    self.labels_set[node].update(sequence[-1]['strings'])
                self.labels_counter.update([label.rsplit('|', maxsplit=1)[-1] for label in sequence[-1]['strings']])
                # get predicted classification on the fly, so we can save to mongo individually
                pred_dict = {node: self.predictions[k][node] for node in self.query_nodes}
                for key in pred_dict:
                    pred_dict[key] = prediction_ensemble_model_classification(pred_dict[key])
                    if pred_dict[key] is None:
                        pred_dict[key] = 'UNKNOWN'
                test_step_info.update({'idx': k, 'predicted': pred_dict, 'actual': self.actuals[k],
                                       'classification_counter': self.labels_counter})
                test_step_info = self.compute_incidental_probabilities(test_step_info=test_step_info)

                # observe answer
                self.agent.observe(sequence[-1], nodes=self.ingress_nodes)

            elif self.test_type == 'emotives_value' or self.test_type == 'emotives_polarity':
                for event in sequence:
                    self.agent.observe(data=event, nodes=self.ingress_nodes)
                    for node in self.ingress_nodes:
                        self.emotives_set[node].update(list(self.agent.get_percept_data()[node]['emotives'].keys()))
                # get and store predictions after observing events
                self.predictions.append(self.agent.get_predictions(nodes=self.query_nodes))
                # store answers in a separate list for evaluation
                self.actuals.append(self.sum_sequence_emotives(sequence))

                pred_dict = {node: self.predictions[k][node] for node in self.query_nodes}
                for key in pred_dict:
                    pred_dict[key] = make_modeled_emotives_(pred_dict[key])

                test_step_info.update({'idx': k, 'predicted': pred_dict, 'actual': self.actuals[-1]})
                test_step_info = self.compute_incidental_probabilities(test_step_info=test_step_info)

            else:
                raise Exception(f"Invalid test type {self.test_type}")

            # prepare test step message
            test_step_msg = PVTMessage(status='testing', current_record=k + 1, total_record_count=test_seq_len,
                                       metrics=test_step_info, cur_test_num=self.test_num, total_test_num=self.num_of_tests,
                                       test_id=self.test_id, user_id=self.user_id, test_type=self.test_type)

            self.store_train_record(test_num=self.test_num, record=test_step_msg)

            # learn answer (optional continous learning)
            if self.test_prediction_strategy == "continuous":
                self.agent.learn(nodes=self.ingress_nodes)
            elif self.test_prediction_strategy == "noncontinuous":
                continue
            else:
                raise Exception(
                    """
                    Not a valid test prediction strategy. Please choose either 'continuous',
                    which means to learn the test sequence/answer after the agent has tried to make a prediction on that test sequence,
                    or, 'noncontinuous', which means to not learn the test sequence.
                    """
                )

    def sum_sequence_emotives(self, sequence):
        """
        Sums all emotive values
        """
        emotives_seq = [event['emotives'] for event in sequence if event['emotives']]
        return dict(functools.reduce(operator.add, map(Counter, emotives_seq)))

    def get_classification_metrics(self):
        """
        Builds classification data structures for each node
        """
        self.class_metrics_data_structures = {}
        for node, labels in self.labels_set.items():
            self.class_metrics_data_structures[node] = classification_metrics_builder(lst_of_labels=labels)
            # Let's see how well the agent scored
            overall_preds = []
            answers       = []
            for p in range(0, len(self.predictions)):
                overall_pred = prediction_ensemble_model_classification(self.predictions[p][node])
                if overall_pred is None:
                    # if the agent doesn't have enough information to make a prediction it wouldn't give one
                    overall_preds.append('UNKNOWN')
                else:
                    overall_preds.append(overall_pred)
                answers.append(self.actuals[p][0])
            try:
                accuracy = round(accuracy_score(answers, overall_preds), 2) * 100
            except ZeroDivisionError:
                accuracy = 0.0
            prec_predictions       = [p for p, a in zip(overall_preds, answers) if p != 'UNKNOWN']
            prec_answers           = [a for p, a in zip(overall_preds, answers) if p != 'UNKNOWN']
            try:
                if len(prec_predictions) == 0:
                    precision = 0.0
                else:
                    precision = round(accuracy_score(prec_answers, prec_predictions), 2) * 100
            except ZeroDivisionError:
                precision = 0.0
            total_amount_of_questions = len(answers)
            updated_pred_length       = len([p for p in overall_preds if p != 'UNKNOWN'])
            try:
                resp_pc = np.round(updated_pred_length / total_amount_of_questions, 2) * 100
            except ZeroDivisionError:
                resp_pc = 0.0

            if math.isnan(precision):
                precision = 0.0

            self.class_metrics_data_structures[node]['predictions']          = overall_preds
            self.class_metrics_data_structures[node]['actuals']              = answers
            self.class_metrics_data_structures[node]['metrics']['resp_pc']   = resp_pc
            self.class_metrics_data_structures[node]['metrics']['accuracy']  = accuracy
            self.class_metrics_data_structures[node]['metrics']['precision'] = precision

    def compute_incidental_probabilities(self, test_step_info: dict):
        """Keep track of how well each node is doing during the testing phase. To be used for live visualizations

        Args:
            test_step_info (dict, required): Dictionary containing information about the current predicted, actual answers, and other related metrics (e.g. precision, unknowns, residuals, response rate, etc.)

        Returns:
            dict: updated test_step_info with the current running accuracy
        """
        idx = test_step_info['idx']

        if self.test_type == 'classification':

            # compute hive prediction for time idx
            hive_pred = hive_model_classification(ensembles=self.predictions[idx])
            if hive_pred is None:
                hive_pred = 'UNKNOWN'
            test_step_info['predicted']['hive'] = hive_pred

            if 'running_accuracy' not in test_step_info:
                test_step_info['true_positive'] = dict()
                test_step_info['false_positive'] = dict()
                test_step_info['unknown_percentage'] = dict()

                test_step_info['running_accuracy'] = dict()
                for k in test_step_info['predicted'].keys():
                    if test_step_info['predicted'][k] in test_step_info['actual']:
                        test_step_info['running_accuracy'][k] = 1.0
                        test_step_info['true_positive'][k] = 1
                        test_step_info['false_positive'][k] = 0

                    else:
                        test_step_info['running_accuracy'][k] = 0.0
                        test_step_info['true_positive'][k] = 0
                        test_step_info['false_positive'][k] = 1

                test_step_info['response_percentage'] = dict()
                test_step_info['response_counts'] = dict()
                test_step_info['running_precisions'] = dict()
                for k in test_step_info['predicted'].keys():
                    if test_step_info['predicted'][k] != 'UNKNOWN':
                        test_step_info['response_percentage'][k] = 1.0
                        test_step_info['response_counts'][k] = 1
                        test_step_info['running_precisions'][k] = test_step_info['running_accuracy'][k]
                    else:
                        test_step_info['response_percentage'][k] = 0.0
                        test_step_info['running_precisions'][k] = 1.0
                        test_step_info['response_counts'][k] = 0

                    test_step_info['unknown_percentage'][k] = 1 - test_step_info['response_percentage'][k]

            else:
                for k in test_step_info['predicted'].keys():
                    if test_step_info['predicted'][k] != 'UNKNOWN':
                        test_step_info['response_counts'][k] += 1

                    if test_step_info['predicted'][k] in test_step_info['actual']:
                        test_step_info['true_positive'][k] += 1
                    else:
                        test_step_info['false_positive'][k] += 1

                    try:
                        test_step_info['running_precisions'][k] = test_step_info['true_positive'][k] / test_step_info['response_counts'][k]
                    except ZeroDivisionError:
                        test_step_info['running_precisions'][k] = 0.0
                        pass

                    test_step_info['running_accuracy'][k] = test_step_info['true_positive'][k] / (idx + 1)
                    test_step_info['response_percentage'][k] = test_step_info['response_counts'][k] / (idx + 1)
                    test_step_info['unknown_percentage'][k] = 1 - test_step_info['response_percentage'][k]

        elif self.test_type == 'emotives_polarity':

            # compute hive prediction for time idx
            test_step_info['predicted']['hive'] = average_emotives(list(test_step_info['predicted'].values()))

            # Initialize metrics on first observation
            if 'running_accuracy' not in test_step_info:
                test_step_info['true_positive']       = defaultdict(dict)
                test_step_info['false_positive']      = defaultdict(dict)
                test_step_info['true_negative']       = defaultdict(dict)
                test_step_info['false_negative']      = defaultdict(dict)
                test_step_info['unknown_percentage']  = defaultdict(dict)
                test_step_info['response_percentage'] = defaultdict(dict)
                test_step_info['response_counts']     = defaultdict(dict)
                test_step_info['running_accuracy']    = defaultdict(dict)
                test_step_info['running_precisions']  = defaultdict(dict)

                for k in test_step_info['predicted'].keys():
                    for emotive in test_step_info['actual'].keys():
                        if emotive in test_step_info['predicted'][k].keys():
                            pred_sign = np.sign(test_step_info['predicted'][k][emotive])
                            actual_sign = np.sign(test_step_info['actual'][emotive])

                            # If actual sign is zero for a polarity test, something is wrong in the data
                            if actual_sign == 0:
                                raise Exception(f'Zero value found in polarity test at idx {idx}')

                            # Check if the predicted sign is zero (unknown) to incremenet response count and percentage
                            if bool(pred_sign):
                                test_step_info['response_counts'][k][emotive] = 1
                                test_step_info['response_percentage'][k][emotive] = 1.0
                                test_step_info['unknown_percentage'][k][emotive] = 0.0
                            else:
                                test_step_info['response_counts'][k][emotive] = 0
                                test_step_info['response_percentage'][k][emotive] = 0.0
                                test_step_info['unknown_percentage'][k][emotive] = 1.0

                            # True positive (correct)
                            if actual_sign > 0 and pred_sign > 0:
                                test_step_info['true_positive'][k][emotive] = 1
                                test_step_info['true_negative'][k][emotive] = 0
                                test_step_info['false_positive'][k][emotive] = 0
                                test_step_info['false_negative'][k][emotive] = 0

                                test_step_info['running_accuracy'][k][emotive] = 1.0

                            # True Negative (correct)
                            elif actual_sign < 0 and not pred_sign > 0:
                                test_step_info['true_positive'][k][emotive] = 0
                                test_step_info['true_negative'][k][emotive] = 1
                                test_step_info['false_positive'][k][emotive] = 0
                                test_step_info['false_negative'][k][emotive] = 0

                                test_step_info['running_accuracy'][k][emotive] = 1.0

                            # False positive (incorrect)
                            elif actual_sign < 0 and not pred_sign < 0:
                                test_step_info['true_positive'][k][emotive] = 0
                                test_step_info['true_negative'][k][emotive] = 0
                                test_step_info['false_positive'][k][emotive] = 1
                                test_step_info['false_negative'][k][emotive] = 0

                                test_step_info['running_accuracy'][k][emotive] = 0.0

                            # False negative (incorrect)
                            elif actual_sign > 0 and not pred_sign > 0:
                                test_step_info['true_positive'][k][emotive] = 0
                                test_step_info['true_negative'][k][emotive] = 0
                                test_step_info['false_positive'][k][emotive] = 0
                                test_step_info['false_negative'][k][emotive] = 1

                                test_step_info['running_accuracy'][k][emotive] = 0.0

                        # Unknown answer
                        else:
                            test_step_info['response_counts'][k][emotive] = 0
                            test_step_info['response_percentage'][k][emotive] = 0.0
                            test_step_info['unknown_percentage'][k][emotive] = 1.0

                # Initialize precision
                for k in test_step_info['predicted'].keys():
                    for emotive in test_step_info['actual'].keys():
                        if emotive in test_step_info['predicted'][k].keys():
                            if bool(test_step_info['predicted'][k][emotive]):
                                test_step_info['running_precisions'][k][emotive] = test_step_info['running_accuracy'][k]
                            else:
                                test_step_info['running_precisions'][k][emotive] = 1.0

            # Not the first observation, so update values
            else:
                for k in test_step_info['predicted'].keys():
                    for emotive in test_step_info['actual'].keys():

                        # catch new emotives, not yet seen on node {k}
                        if emotive not in test_step_info['true_positive'][k].keys():
                            init_emotive_on_node(emotive=emotive, test_step_info=test_step_info, node=k)
                        if emotive in test_step_info['predicted'][k].keys():
                            pred_sign = np.sign(test_step_info['predicted'][k][emotive])
                            actual_sign = np.sign(test_step_info['actual'][emotive])

                            # else:
                                # print(f'predicted val: {test_step_info["predicted"][k][emotive]}, actual: {test_step_info["actual"][emotive]}')
                            # Polarity error at for zero actual value
                            if actual_sign == 0:
                                raise Exception(f'Zero value found in polarity test at idx {idx}')

                            # If predicted value non-zero
                            if bool(pred_sign):
                                test_step_info['response_counts'][k][emotive] += 1

                            # True positive (correct)
                            if actual_sign > 0 and pred_sign > 0:
                                test_step_info['true_positive'][k][emotive] += 1

                            # True Negative (correct)
                            elif actual_sign < 0 and pred_sign < 0:
                                test_step_info['true_negative'][k][emotive] += 1

                            # False positive (incorrect)
                            elif actual_sign < 0 and not pred_sign < 0:
                                test_step_info['false_positive'][k][emotive] += 1

                            # False negative (incorrect)
                            elif actual_sign > 0 and not pred_sign > 0:
                                test_step_info['false_negative'][k][emotive] += 1

                            # Calculate precision value
                            try:
                                test_step_info['running_precisions'][k][emotive] = (test_step_info['true_positive'][k][emotive] + test_step_info['true_negative'][k][emotive]) / test_step_info['response_counts'][k][emotive]
                            except ZeroDivisionError:
                                test_step_info['running_precisions'][k][emotive] = 0.0

                            test_step_info['running_accuracy'][k][emotive] = (test_step_info['true_positive'][k][emotive] + test_step_info['true_negative'][k][emotive]) / (idx + 1)

                        # Update response percentage and unknown percentage
                        test_step_info['response_percentage'][k][emotive] = test_step_info['response_counts'][k][emotive] / (idx + 1)
                        test_step_info['unknown_percentage'][k][emotive] = 1 - test_step_info['response_percentage'][k][emotive]

        elif self.test_type == 'emotives_value':
            test_step_info['predicted']['hive'] = average_emotives(list(test_step_info['predicted'].values()))
            # Initialize metrics on first observation
            if 'running_accuracy' not in test_step_info:
                test_step_info['unknown_percentage']  = defaultdict(dict)
                test_step_info['response_percentage'] = defaultdict(dict)
                test_step_info['response_counts']     = defaultdict(dict)
                test_step_info['residuals']           = defaultdict(dict)
                test_step_info['abs_residuals']       = defaultdict(dict)
                test_step_info['squared_residuals']   = defaultdict(dict)

                for k in test_step_info['predicted'].keys():
                    for emotive in test_step_info['actual'].keys():
                        if emotive in test_step_info['predicted'][k].keys():
                            test_step_info['residuals'][k][emotive] = test_step_info['actual'][emotive] - test_step_info['predicted'][k][emotive]
                            test_step_info['abs_residuals'][k][emotive] = abs(test_step_info['actual'][emotive] - test_step_info['predicted'][k][emotive])
                            test_step_info['squared_residuals'][k][emotive] = math.pow(test_step_info['actual'][emotive] - test_step_info['predicted'][k][emotive], 2)
                            test_step_info['response_counts'][k][emotive] = 1
                            test_step_info['response_percentage'][k][emotive] = 1.0
                            test_step_info['unknown_percentage'][k][emotive] = 0.0

                        # Unknown answer
                        else:
                            test_step_info['residuals'][k] = defaultdict(float)
                            test_step_info['response_counts'][k][emotive] = 0
                            test_step_info['response_percentage'][k][emotive] = 0.0
                            test_step_info['unknown_percentage'][k][emotive] = 1.0

            # Not the first observation, so update values
            else:
                for emotive in test_step_info['actual'].keys():
                    if emotive in test_step_info['predicted'][k].keys():

                        test_step_info['residuals'][k][emotive] = test_step_info['actual'][emotive] - test_step_info['predicted'][k][emotive]
                        test_step_info['response_counts'][k][emotive] += 1

                    # Update response percentage and unknown percentage
                    test_step_info['response_percentage'][k][emotive] = test_step_info['response_counts'][k][emotive] / (idx + 1)
                    test_step_info['unknown_percentage'][k][emotive] = 1 - test_step_info['response_percentage'][k][emotive]

        else:
            raise Exception('Unknown test type')

        return test_step_info

    def get_emotives_value_metrics(self):
        """
        Builds emotives value data structures for each node
        """
        # Build an emotives Metric Data Structure
        self.emotives_metrics_data_structures = {}
        for node, emotive_set in self.emotives_set.items():
            self.emotives_metrics_data_structures[node] = emotives_value_metrics_builder(lst_of_emotives=list(emotive_set))

        # Populate Emotives Metrics
        for i, (prediction_ensemble, actual) in enumerate(zip(self.predictions, self.actuals)):
            for node_name, node_pred_ensemble in prediction_ensemble.items():
                if node_pred_ensemble:
                    modeled_emotives = make_modeled_emotives_(ensemble=node_pred_ensemble)  # get overall prediction from a single node
                    for emotive_name_from_model, pred_value in modeled_emotives.items():
                        if emotive_name_from_model in list(self.emotives_metrics_data_structures[node_name].keys()):
                            self.emotives_metrics_data_structures[node_name][emotive_name_from_model]['predictions'].append(pred_value)
                            self.emotives_metrics_data_structures[node_name][emotive_name_from_model]['actuals'].append(retrieve_emotive_val(emotive_name_from_model, actual))
                    left_overs = set(self.emotives_metrics_data_structures) - set(list(modeled_emotives.keys()))
                    if left_overs:
                        for emotive_name, metric_data in self.emotives_metrics_data_structures[node_name].items():
                            if emotive_name in left_overs:
                                self.emotives_metrics_data_structures[node_name][emotive_name]['predictions'].append(np.nan)
                                self.emotives_metrics_data_structures[node_name][emotive_name]['actuals'].append(retrieve_emotive_val(emotive_name, actual))
                else:
                    for emotive_name, metric_data in self.emotives_metrics_data_structures[node_name].items():
                        self.emotives_metrics_data_structures[node_name][emotive_name]['predictions'].append(np.nan)
                        self.emotives_metrics_data_structures[node_name][emotive_name]['actuals'].append(retrieve_emotive_val(emotive_name, actual))
                # Create Metrics
                for node_name, node_emotive_metrics in self.emotives_metrics_data_structures.items():
                    # calculate response rate percentage
                    for emotive_name, data in node_emotive_metrics.items():
                        total_amount_of_questions            = len(data['actuals'])
                        updated_pred_length                  = len([p for p in data['predictions'] if p is not np.nan])
                        try:
                            resp_pc = np.round(updated_pred_length / total_amount_of_questions, 2) * 100
                        except ZeroDivisionError:
                            resp_pc = 0.0
                        self.emotives_metrics_data_structures[node_name][emotive_name]['metrics']['resp_pc'] = resp_pc
                    # calculate rmse
                    for emotive_name, data in node_emotive_metrics.items():
                        error_lst = [p - a for p, a in zip(data['predictions'], data['actuals']) if p is not np.nan]
                        if error_lst:
                            rmse = math.sqrt(np.square(error_lst).mean())
                            self.emotives_metrics_data_structures[node_name][emotive_name]['metrics']['rmse'] = rmse
                    # calculate smape_precision
                    for emotive_name, data in node_emotive_metrics.items():
                        smape_prec_predictions       = [p for p, a in zip(data['predictions'], data['actuals']) if p is not np.nan]
                        smape_prec_actuals           = [a for p, a in zip(data['predictions'], data['actuals']) if p is not np.nan]
                        smape_prec_predictions_array = np.array(smape_prec_predictions)
                        smape_prec_actuals_array     = np.array(smape_prec_actuals)

                        forecast_diff = np.abs(smape_prec_predictions_array - smape_prec_actuals_array)
                        forecast_sum  = (np.abs(smape_prec_actuals_array) + np.abs(smape_prec_predictions_array)) / 2
                        smape_elements = forecast_diff / forecast_sum

                        try:
                            smape = (1 - (np.nansum(smape_elements) / len(smape_prec_actuals_array))) * 100
                        except ZeroDivisionError:
                            smape = None
                        self.emotives_metrics_data_structures[node_name][emotive_name]['metrics']['smape_prec'] = smape

    def get_emotives_polarity_metrics(self):
        """
        Builds emotives polarity data structures for each node
        """
        template_dict = {'true_positive': {},
                         'false_positive': {},
                         'true_negative': {},
                         'false_negative': {},
                         'unknown_percentage': {},
                         'response_percentage':{},
                         'response_counts': {},
                         'running_accuracy': {},
                         'running_precisions': {}
                        }
        if len(self.testing_log[self.test_num]) == 0:
            return {}
        # lets flip the dictionary so that it is organized per node instead of per metric
        raw_test_results = deepcopy(self.testing_log[self.test_num][-1]['metrics'])

        flattened_emotive_set = set(chain(*[list(item) for item in self.emotives_set.values()]))
        hive_emotives = flattened_emotive_set
        emo_res2 = {k: {i: deepcopy(template_dict) for i in v } for k, v in self.emotives_set.items()}
        emo_res2['hive'] = {emo: deepcopy(template_dict) for emo in hive_emotives}
        emotive_results = {k: deepcopy(template_dict) for k in flattened_emotive_set}
        # print(f'before: {emotive_results=}')
        for k, v in raw_test_results.items():
            if k in ['idx', 'predicted', 'actual']:
                continue

            for node, info in v.items():
                for emotive, emotive_data in info.items():
                    emotive_results[emotive][k][node] = deepcopy(emotive_data)
                    if emotive in emo_res2[node]:
                        emo_res2[node][emotive][k] = deepcopy(emotive_data)


        return emo_res2

        # Build an emotives Metric Data Structure
        self.emotives_metrics_data_structures = {}
        for node, emotive_set in self.emotives_set.items():
            self.emotives_metrics_data_structures[node] = emotives_polarity_metrics_builder(lst_of_emotives=list(emotive_set))
        # Populate Emotives Metrics
        for i, (prediction_ensemble, actual) in enumerate(zip(self.predictions, self.actuals)):
            for node_name, node_pred_ensemble in prediction_ensemble.items():
                if node_pred_ensemble:
                    modeled_emotives = make_modeled_emotives_(ensemble=node_pred_ensemble)  # get overall prediction from a single node
                    for emotive_name_from_model, pred_value in modeled_emotives.items():
                        if emotive_name_from_model in list(self.emotives_metrics_data_structures[node_name].keys()):
                            self.emotives_metrics_data_structures[node_name][emotive_name_from_model]['predictions'].append(pred_value)
                            self.emotives_metrics_data_structures[node_name][emotive_name_from_model]['actuals'].append(retrieve_emotive_val(emotive_name_from_model, actual))
                    left_overs = set(self.emotives_metrics_data_structures) - set(list(modeled_emotives.keys()))
                    if left_overs:
                        for emotive_name, metric_data in self.emotives_metrics_data_structures[node_name].items():
                            if emotive_name in left_overs:
                                self.emotives_metrics_data_structures[node_name][emotive_name]['predictions'].append(np.nan)
                                self.emotives_metrics_data_structures[node_name][emotive_name]['actuals'].append(retrieve_emotive_val(emotive_name, actual))
                else:
                    for emotive_name, metric_data in self.emotives_metrics_data_structures[node_name].items():
                        self.emotives_metrics_data_structures[node_name][emotive_name]['predictions'].append(np.nan)
                        self.emotives_metrics_data_structures[node_name][emotive_name]['actuals'].append(retrieve_emotive_val(emotive_name, actual))
                # Create Metrics
                for node_name, node_emotive_metrics in self.emotives_metrics_data_structures.items():
                    # calculate response rate percentage
                    for emotive_name, data in node_emotive_metrics.items():
                        total_amount_of_questions            = len(data['actuals'])
                        updated_pred_length                  = len([p for p in data['predictions'] if p is not np.nan])
                        try:
                            resp_pc = np.round(updated_pred_length / total_amount_of_questions, 2) * 100
                        except ZeroDivisionError:
                            resp_pc = 0.0
                        self.emotives_metrics_data_structures[node_name][emotive_name]['metrics']['resp_pc'] = resp_pc
                    # calculate accuracy
                    for emotive_name, data in node_emotive_metrics.items():
                        polarity_accuracy_loading_dock = []
                        polarity_precision_loading_dock = []
                        for p, a in zip(data['predictions'], data['actuals']):
                            if p is np.nan:
                                polarity_accuracy_loading_dock.append("incorrect")
                            elif p is not np.nan:
                                if p * a > 0:
                                    polarity_accuracy_loading_dock.append("correct")
                                elif p * a < 0:
                                    polarity_accuracy_loading_dock.append("incorrect")
                            else:
                                raise Exception("Something is wrong with the data type...")
                        try:
                            accuracy = round(polarity_accuracy_loading_dock.count("correct") / len(polarity_accuracy_loading_dock), 2) * 100
                        except ZeroDivisionError():
                            accuracy = 0.0
                        # populate accuracy to data structure
                        self.emotives_metrics_data_structures[node_name][emotive_name]['metrics']['accuracy'] = accuracy
                        # calculate precision
                        for p, a in zip(data['predictions'], data['actuals']):
                            if p is np.nan:
                                continue
                            elif p is not np.nan:
                                if p * a > 0:
                                    polarity_precision_loading_dock.append("correct")
                                elif p * a < 0:
                                    polarity_precision_loading_dock.append("incorrect")
                            else:
                                raise Exception("Something is wrong with the data type...")
                        try:
                            precision = round(polarity_precision_loading_dock.count("correct") / len(polarity_precision_loading_dock),
                                              2) * 100
                        except ZeroDivisionError():
                            precision = 0.0
                        # populate precision to data structure
                        self.emotives_metrics_data_structures[node_name][emotive_name]['metrics']['precision'] = precision

    def update_test_results_w_hive_classification_metrics(self, pvt_test_result):
        """
        Update pvt test result metrics with hive classifications metrics
        """
        # add hive_metrics
        hive_metrics = {
            'predictions': [],
            'actuals': [],
            'labels': [],
            'metrics': {
                'resp_pc': None,
                'accuracy': None,
                'precision': None
            }
        }

        # get hive labels set
        hive_label_count = []
        for node_name, test_data in pvt_test_result.items():
            if node_name != 'hive':
                for label in test_data['labels']:
                    hive_label_count.append(label)

        hive_label_set_lst = list(set(hive_label_count))

        # add hive metrics dictionary to pvt results
        pvt_test_result['hive'] = hive_metrics

        pvt_test_result['hive']['labels'] = hive_label_set_lst

        # get predictions to get hive classification of all nodes
        for i in range(0, len(self.predictions)):
            pred = hive_model_classification(ensembles=self.predictions[i])
            if pred is None:
                pred = 'UNKNOWN'
            pvt_test_result['hive']['predictions'].append(deepcopy(pred))

        # get actuals of test
        for i in range(0, len(self.actuals)):
            pvt_test_result['hive']['actuals'].append(self.actuals[i][0])

        # get hive accuracy of test
        for node_name, test_data in pvt_test_result.items():
            if node_name == 'hive':
                try:
                    hive_accuracy = round(accuracy_score(test_data['actuals'], test_data["predictions"]), 2) * 100
                except ZeroDivisionError:
                    hive_accuracy = 0.0
        pvt_test_result['hive']['metrics']['accuracy'] = hive_accuracy

        # get hive precision of test
        for node_name, test_data in pvt_test_result.items():
            if node_name == 'hive':

                prec_predictions       = [p for p, _ in zip(test_data["predictions"], test_data['actuals']) if p != 'UNKNOWN']
                prec_answers           = [a for p, a in zip(test_data["predictions"], test_data['actuals']) if p != 'UNKNOWN']
                try:
                    hive_precision = round(accuracy_score(prec_answers, prec_predictions), 2) * 100
                except ZeroDivisionError:
                    hive_precision = 0.0
        pvt_test_result['hive']['metrics']['precision'] = hive_precision

        # get hive response rate percentage of test
        for node_name, test_data in pvt_test_result.items():
            if node_name == 'hive':
                total_amount_of_questions            = len(test_data['actuals'])
                updated_pred_length                  = len([p for p in test_data["predictions"] if p != 'UNKNOWN'])
                try:
                    hive_resp_pc = np.round(updated_pred_length / total_amount_of_questions, 2) * 100
                except ZeroDivisionError:
                    hive_resp_pc = 0.0
        pvt_test_result['hive']['metrics']['resp_pc'] = hive_resp_pc

        return pvt_test_result

    def update_test_results_w_hive_emotives_value_metrics(self, pvt_test_result):
        """
        Update pvt test result metrics with hive classifications metrics
        """
        all_nodes_emotives_set = set()
        for node, emotives in self.emotives_set.items():
            for emotive in emotives:
                all_nodes_emotives_set.add(emotive)
        hive_emotives_value_metrics_lst = []
        for emotive in all_nodes_emotives_set:
            hive_emotives_value_metrics_template = {
                f'{emotive}': {
                    'metrics': {
                        'resp_pc': [],
                        'rmse': [],
                        'smape_prec': []
                    },
                    # 'predictions' : {node: [] for node in self.emotives_set},
                    # 'actuals' : {node: [] for node in self.emotives_set}
                }
            }
            hive_emotives_value_metrics_lst.append(hive_emotives_value_metrics_template)

        for test_metric in self.pvt_results:
            for test_data in test_metric.values():
                for emotive, emotive_metric in test_data.items():
                    if emotive_metric['metrics']['resp_pc'] != 0.0 and emotive in all_nodes_emotives_set:
                        for hive_emotive_metric_dict in hive_emotives_value_metrics_lst:
                            if emotive in hive_emotive_metric_dict.keys():
                                hive_emotive_metric_dict[emotive]['metrics']['resp_pc'].append(emotive_metric['metrics']['resp_pc'])
                                hive_emotive_metric_dict[emotive]['metrics']['rmse'].append(emotive_metric['metrics']['rmse'])
                                hive_emotive_metric_dict[emotive]['metrics']['smape_prec'].append(emotive_metric['metrics']['smape_prec'])

        # average emotive metrics into one final result
        for emotive_metrics in hive_emotives_value_metrics_lst:
            for emotive_name, metric_data in emotive_metrics.items():
                for metric_name, metric_data_lst in metric_data['metrics'].items():
                    if len(metric_data_lst) == 0:
                        continue
                    emotive_metrics[emotive_name]['metrics'][metric_name] = sum(metric_data_lst) / len(metric_data_lst)

        # flatten list of dicts to single dict
        hive_emotive_overall_dict = {}
        for emo_dict in hive_emotives_value_metrics_lst:
            hive_emotive_overall_dict.update(**emo_dict)

        pvt_test_result['hive'] = hive_emotive_overall_dict
        return pvt_test_result

    def update_test_results_w_hive_emotives_polarity_metrics(self, pvt_test_result):
        """
        Update pvt test result metrics with hive emotives polarity metrics
        """
        all_nodes_emotives_set = set()
        for node, emotives in self.emotives_set.items():
            for emotive in emotives:
                all_nodes_emotives_set.add(emotive)
        hive_emotives_value_metrics_lst = []
        for emotive in all_nodes_emotives_set:
            hive_emotives_value_metrics_template = {
                f'{emotive}': {
                    'metrics': {
                        'resp_pc': [],
                        'accuracy': [],
                        'precision': []
                    }
                }
            }
            hive_emotives_value_metrics_lst.append(hive_emotives_value_metrics_template)
        for test_metric in self.pvt_results:
            for test_data in test_metric.values():
                for emotive, emotive_metric in test_data.items():
                    if emotive_metric['metrics']['resp_pc'] != 0.0 and emotive in all_nodes_emotives_set:
                        for hive_emotive_metric_dict in hive_emotives_value_metrics_lst:
                            if emotive in hive_emotive_metric_dict.keys():
                                hive_emotive_metric_dict[emotive]['metrics']['resp_pc'].append(emotive_metric['metrics']['resp_pc'])
                                hive_emotive_metric_dict[emotive]['metrics']['accuracy'].append(emotive_metric['metrics']['accuracy'])
                                hive_emotive_metric_dict[emotive]['metrics']['precision'].append(emotive_metric['metrics']['precision'])
        for emotive_metrics in hive_emotives_value_metrics_lst:
            for emotive_name, metric_data in emotive_metrics.items():
                for metric_name, metric_data_lst in metric_data['metrics'].items():
                    if len(metric_data_lst) == 0:
                        continue
                    emotive_metrics[emotive_name]['metrics'][metric_name] = sum(metric_data_lst) / len(metric_data_lst)

        hive_emotive_overall_dict = {}
        for emo_dict in hive_emotives_value_metrics_lst:
            hive_emotive_overall_dict.update(**emo_dict)

        if not self.QUIET:
            print(f'{hive_emotive_overall_dict=}')
        pvt_test_result['hive'] = hive_emotive_overall_dict
        return pvt_test_result

    def plot_emotives_value_charts(self, test_num):

        for node_name, node_emotive_metrics in self.emotives_metrics_data_structures.items():
            if not self.QUIET:
                print(f'-----------------Test#{test_num}-{node_name}-Plots-----------------')
            for emotive_name, data in sorted(node_emotive_metrics.items()):
                labels = 'precision', 'miss'
                if data['metrics']['smape_prec'] is None:
                    sizes = [0, 100]
                else:
                    sizes = [data['metrics']['smape_prec'], 100 - data['metrics']['smape_prec']]
                explode = (0, 0)
                _, ax1 = plt.subplots()
                ax1.title.set_text(f'{node_name} - {emotive_name}')
                ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                        shadow=True, startangle=90)
                ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                colors = ['gray', 'skyblue']
                patches, texts = plt.pie(sizes, colors=colors, startangle=90)
                plt.legend(patches, labels, loc="best")
                plt.figtext(0, 0, f"{pd.Series(data['metrics']).round(1).to_string()}", ha="center", fontsize=18, bbox={"facecolor": "orange", "alpha": 0.5, "pad": 5})
                try:
                    plt.savefig(f"{self.results_filepath}/{test_num}_{node_name}_{emotive_name}.png", dpi=300, bbox_inches='tight')
                except Exception as e:
                    if not self.QUIET:
                        print(f"Not able to save figure in assigned results directory! Please add an appropriate directory: {str(e)}")
                    pass
                plt.show()
                if not self.QUIET:
                    print('---------------------')

    def abort_test_remediation(self, current_record, record_count):
        if not self.QUIET:
            print(f'about to abort {self.task.request.id =}, {self.test_id=}')
        if self.sio:
            if not self.QUIET:
                print('Sending abort message')
            abort_msg = PVTMessage(status='aborted', current_record=current_record + 1, total_record_count=record_count,
                                    metrics={}, cur_test_num=self.test_num, total_test_num=self.num_of_tests,
                                    test_id=self.test_id, user_id=self.user_id, test_type=self.test_type)
            self.sio.emit(self.socket_channel, abort_msg.toJSON(), to=self.user_id)
        if self.mongo_results:
            if not self.QUIET:
                print('cleaning up MongoDB')
            self.mongo_results.deleteResults()

        raise PVTAbortError(f"Aborting Test, at record {current_record} of {record_count}")

    def store_train_record(self, test_num, record: PVTMessage):
        
        if record.status == 'testing':
            self.testing_log[test_num].append(deepcopy(record.toJSON()))

        # insert into test_log in mongo, if using mongodb
        if self.mongo_results:
            self.mongo_results.addLogRecord(type=record.status, record=deepcopy(record.toJSON()))

        # emit socketIO message
        if self.sio:
            self.sio.emit(self.socket_channel, deepcopy(record.toJSON()), to=self.user_id)