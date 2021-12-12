from flappy_agent import FlappyAgent
from flappy_env import Environment
import matplotlib.pyplot as plt
import time

# For plotting metrics
epoch_iterations_list = []
epoch_rewards_list = []
best_epoch_reward_sum = -1
best_epoch = 0

n_iterations = int(15e5)
iteration = 0
epoch = 0

print_epoch_interval = 500

env = Environment()
agent = FlappyAgent(observation_space_size=env.observation_space_size,
                    action_space=env.action_space,
                    n_iterations=n_iterations)

start_time = time.time()
while iteration < n_iterations:
    state = env.reset()

    epoch_iteration, epoch_reward_sum = 0, 0
    done = False

    while not done:
        action = agent.step(state)
        next_state, reward, done, info = env.step(action)
        agent.learn(state, action, next_state, reward)

        state = next_state

        epoch_iteration += 1
        epoch_reward_sum += reward
        
        iteration += 1

    if epoch_reward_sum > best_epoch_reward_sum:
        best_epoch_reward_sum = epoch_reward_sum
        best_epoch = epoch

    agent.epoch_end(epoch_reward_sum)

    if epoch % print_epoch_interval == 0:
        print('\nEpoch:', epoch)
        print('Iteration: {} ({:.02f}%)'.format(iteration, 100 * iteration / n_iterations))
        print('Best aggregate reward:', best_epoch_reward_sum)

    epoch_iterations_list.append(epoch_iteration)
    epoch_rewards_list.append(epoch_reward_sum)
    
    epoch += 1

agent.train_end()

print('Training finished.\n')
print('Last 10 iterations:', epoch_iterations_list[-10:])
print('Last 10 aggregate rewards:', epoch_rewards_list[-10:])
print('Best aggregate reward:', best_epoch_reward_sum)
print('Best epoch:', best_epoch)
print('Training Duration: %.2f seconds' % (time.time() - start_time))
fig, ax = plt.subplots(1,2)
ax[0].scatter(range(len(epoch_iterations_list)), epoch_iterations_list, label='Iterations')
ax[0].legend()
ax[1].scatter(range(len(epoch_rewards_list)), epoch_rewards_list, label='Aggregate rewards')
ax[1].legend()
plt.show()

print('Starting test.')

n_max_reward = 25
n_test_run = 100
reward_avg_all = 0

for _ in range(n_test_run):
    test_iteration = 0
    reward_sum = 0
    done = False
    state = env.reset()

    while not done and reward_sum < n_max_reward:
        action = agent.step(state)
        state, reward, done, _ = env.step(action)

        reward_sum += reward
        test_iteration += 1

    reward_avg_all += reward_sum
    print('Iterations:', test_iteration)
    print('Aggregate test reward:', reward_sum)

reward_avg_all /= n_test_run
print('Average reward:', reward_avg_all);
