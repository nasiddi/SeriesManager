-- Up

CREATE TABLE IF NOT EXISTS algorithms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    description TEXT,
    description_source TEXT,
    config_base TEXT DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS algorithm_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    algorithm_id INTEGER,
    name TEXT,
    description TEXT DEFAULT null
);


INSERT INTO `algorithms`
    (`id`, `name`, `description`, `description_source`, `config_base`)
    VALUES
    (
        1,
        'Naive Bayes',
        "In machine learning, naive Bayes classifiers are a family of simple probabilistic classifiers based on applying Bayes' theorem with strong (naive) independence assumptions between the features.",
        'https://en.wikipedia.org/wiki/Naive_Bayes_classifier',
        '{"classifier": "NB"}'
    ),
    (
        2,
        'Support Vector Machine',
        "In machine learning, support vector machines (SVMs, also support vector networks) are supervised learning models with associated learning algorithms that analyze data used for classification and regression analysis. Given a set of training examples, each marked as belonging to one or the other of two categories, an SVM training algorithm builds a model that assigns new examples to one category or the other, making it a non-probabilistic binary linear classifier (although methods such as Platt scaling exist to use SVM in a probabilistic classification setting).",
        'https://en.wikipedia.org/wiki/Support_vector_machine',
        '{"classifier": "SVM"}'
    ),
    (
        3,
        'Stochastic Gradient Descent',
        "Stochastic Gradient Descent (SGD) is a simple yet very efficient approach to discriminative learning of linear classifiers under convex loss functions such as (linear) Support Vector Machines and Logistic Regression. Even though SGD has been around in the machine learning community for a long time, it has received a considerable amount of attention just recently in the context of large-scale learning.",
        'http://scikit-learn.org/stable/modules/sgd.html',
        '{"classifier": "SGD"}'
    ),
    (
        4,
        'AdaBoost',
        "An AdaBoost classifier is a meta-estimator that begins by fitting a classifier on the original dataset and then fits additional copies of the classifier on the same dataset but where the weights of incorrectly classified instances are adjusted such that subsequent classifiers focus more on difficult cases.",
        'http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html',
        '{"classifier": "ADA"}'
    ),
    (
        5,
        'Convolutional neural network',
        "In machine learning, a convolutional neural network (CNN, or ConvNet) is a class of deep, feed-forward artificial neural networks that has successfully been applied to analyzing visual imagery. CNNs use a variation of multilayer perceptrons designed to require minimal preprocessing. They are also known as shift invariant or space invariant artificial neural networks (SIANN), based on their shared-weights architecture and translation invariance characteristics. Convolutional networks were inspired by biological processes in that the connectivity pattern between neurons resembles the organization of the animal visual cortex. Individual cortical neurons respond to stimuli only in a restricted region of the visual field known as the receptive field. The receptive fields of different neurons partially overlap such that they cover the entire visual field.",
        'https://en.wikipedia.org/wiki/Convolutional_neural_network',
        '{"classifier": "CNN"}'
    )
;

INSERT INTO `algorithm_configs`
    (`algorithm_id`, `name`)
    VALUES
    (1, 'run'),
    (2, 'run'),
    (3, 'run'),
    (4, 'run'),
    (5, 'run')
;

-- Down

DROP TABLE algorithms;

DROP TABLE algorithm_configs;
