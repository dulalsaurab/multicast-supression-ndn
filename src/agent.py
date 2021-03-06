import tensorflow as tf
from tensorflow.keras.optimizers import Adam
import tensorflow_probability as tfp
from network import ActorCriticNetwork

class Agent:
    def __init__(self, alpha=0.0003, gamma=0.99, n_actions=4):
        self.gamma = gamma
        self.n_actions = n_actions
        self.action = None      #keep track of last action
        self.action_space = [i for i in range(self.n_actions)] #random action selection
        self.actor_critic = ActorCriticNetwork(n_actions=n_actions)
        self.actor_critic.compile(optimizer=Adam(learning_rate=alpha))

    def choose_action(self, observation):
        state = tf.convert_to_tensor([observation])
        _, probs = self.actor_critic(state)     #feed through neural network
        action_probabilities = tfp.distributions.Normal(loc=probs[0][0], scale=probs[0][1])
        action = action_probabilities.sample()
        log_prob = action_probabilities.log_prob(action)
        self.action = action
        return action.numpy()

    def save_models(self):
        print('... saving models ...')
        self.actor_critic.save_weights(self.actor_critic.checkpoint_file)

    def load_models(self):
        print('... loading models ...')
        self.actor_critic.load_weights(self.actor_critic.checkpoint_file)
        
    def learn(self, state, reward, state_, done):                       #this is the train
        state = tf.convert_to_tensor([state], dtype=tf.float32)
        state_ = tf.convert_to_tensor([state_], dtype=tf.float32)
        reward = tf.convert_to_tensor(reward, dtype=tf.float32) # not fed to NN
        print ("*******", "state:", state_, "_state", state_)
        with tf.GradientTape() as tape:
            state_value, probs = self.actor_critic(state)
            state_value_, _ = self.actor_critic(state_)
            state_value = tf.squeeze(state_value)
            state_value_ = tf.squeeze(state_value_)
            print ("###########", "state_value: ", state_value)
            action_probs = tfp.distributions.Normal(loc=probs[0][0], scale=probs[0][1])
            log_prob = action_probs.log_prob(self.action)

            delta = reward + self.gamma*state_value_*(1-int(done)) - state_value
            print ("old-state-value: ", state_value, "new-state-value", state_value_, "delta: ", delta)
            actor_loss = -log_prob*delta
            critic_loss = delta**2
            total_loss = actor_loss + critic_loss

        gradient = tape.gradient(total_loss, self.actor_critic.trainable_variables)
        self.actor_critic.optimizer.apply_gradients(zip(gradient, self.actor_critic.trainable_variables))
