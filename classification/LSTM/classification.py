import json

from tuning import tune_parameters
from data_loader import dataset_processing
from train import training, testing
'''
# make the dataset
pos_weight = dataset_processing()
print(pos_weight)

# tune the model
best_parameters = tune_parameters(pos_weight=pos_weight)

# best parameters are selected. View test-set metrics
print(f'Best hyperparameters were: {best_parameters}')
# store best parameters into a file
with open('best_parameters_same_sets.txt', 'w') as f:
    f.write(json.dumps(best_parameters))

f.close()
'''
# now access the best parameters in order to train final model

# reading the data from the file
with open('best_parameters_same_sets.txt') as f:
    data = f.read()

best_parameters_loaded = json.loads(data)
print(best_parameters_loaded)

print('\nNow training with the best parameters\n')
training(params=best_parameters_loaded, make_err_logs=True)

print('\nResults on the test set:\n')
testing(params=best_parameters_loaded)

# CHECK WITH UNSEEN DATA

# make the dataset
'''
pos_weight = dataset_processing(separate_test=True)
print(pos_weight)

# tune the model
best_parameters = tune_parameters(pos_weight=pos_weight)

# best parameters are selected. View test-set metrics
print(f'Best hyperparameters were: {best_parameters}')
# store best parameters into a file
with open('best_parameters_diff_test.txt', 'w') as f:
    f.write(json.dumps(best_parameters))

f.close()

# now access the best parameters in order to train final model

# reading the data from the file
with open('best_parameters_diff_test.txt') as f:
    data = f.read()

best_parameters_loaded = json.loads(data)
print(best_parameters_loaded)

print('\nNow training with the best parameters\n')
valid_error = training(params=best_parameters_loaded, make_err_logs=True)
print(f'Validation error was: {valid_error}')

print('\nResults on the test set:\n')
testing(params=best_parameters_loaded)
'''