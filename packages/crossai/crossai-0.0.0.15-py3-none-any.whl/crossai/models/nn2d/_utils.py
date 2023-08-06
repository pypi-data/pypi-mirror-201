import tensorflow as tf

class DenseDropBlock(tf.keras.Model):
    def __init__(self, n_layers, dense_units, drop_rate, drop_first=False, activation="relu"):
        super().__init__()
        self.layer_list = list()
        for d in range(0, n_layers):
            drop = tf.keras.layers.Dropout(drop_rate[d])
            dense = tf.keras.layers.Dense(units=dense_units[d], 
                                          activation=activation, 
                                          kernel_initializer=tf.keras.initializers.HeUniform(),
                                          kernel_regularizer=tf.keras.regularizers.L2(0.00001), 
                                          kernel_constraint=tf.keras.constraints.max_norm(3)
                                        )
            if drop_first:
                self.layer_list.append(drop)
                self.layer_list.append(dense)
            else:
                self.layer_list.append(dense)
                self.layer_list.append(drop)

    def call(self, inputs):
        x = inputs
        for layer in self.layer_list:
            x = layer(x)
        return x



class DenseBlock(tf.keras.Model):
    def __init__(self, n_layers, dense_units, activation="relu"):
        super(DenseBlock, self).__init__()
        self.dense_list = list()
        for d in range(0, n_layers):
            dense = tf.keras.layers.Dense(units=dense_units[d], 
                                          activation=activation, 
                                          kernel_initializer=tf.keras.initializers.HeUniform(),
                                          kernel_regularizer=tf.keras.regularizers.L2(0.00001), 
                                          kernel_constraint=tf.keras.constraints.max_norm(3)
                                        )
            self.dense_list.append(dense)

    def call(self, inputs):
        x = inputs
        for dense in self.dense_list:
            x = dense(x)
        return x