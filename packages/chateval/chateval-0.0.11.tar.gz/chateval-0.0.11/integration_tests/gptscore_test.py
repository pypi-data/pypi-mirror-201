import unittest

from chateval.metrics import get_metric


class MyTestCase(unittest.TestCase):
    dataset = [{"input": "write a movie review of Titanic"}]
    predictions = [
        'James Cameron\'s 1997 epic romantic disaster film "Titanic" tells the '
        "tragic story of two star-crossed lovers, Jack (Leonardo DiCaprio) and "
        "Rose (Kate Winslet), who fall in love aboard the ill-fated ship that met "
        "its infamous end in the North Atlantic on April 15, 1912. The film was a "
        "commercial and critical success, grossing over $2 billion worldwide "
        "and winning eleven Academy Awards, including Best Picture, Best Director, "
        'and Best Original Song. One of the most impressive aspects of "Titanic" '
        "is the film's stunning visual effects and production design. The "
        "detailed recreation of the Titanic and its sinking is both breathtaking "
        "and haunting, capturing the grandeur and tragedy of the ship's fate. The "
        "special effects used to bring the ship to life and simulate the sinking"
        " are still impressive more than two decades later. Another strong point "
        "of the film is the performances of the two leads, DiCaprio and Winslet. "
        "Their chemistry is palpable and their portrayal of two individuals from "
        "different social classes falling in love against all odds is touching and "
        "believable. The supporting cast, including Billy Zane and Gloria Stuart, "
        "also deliver strong performances that add depth to the film's characters"
        '. At its core, "Titanic" is a poignant love story set against the '
        "backdrop of a tragic historical event. The film expertly blends elements "
        "of romance, drama, and action to create an unforgettable cinematic "
        "experience. Despite its lengthy runtime of over three hours, the film is "
        "engaging and emotionally gripping throughout, leaving a lasting "
        'impression on viewers. Overall, "Titanic" is a cinematic masterpiece '
        "that stands the test of time. Cameron's epic film is a must-see for "
        "fans of romance, drama, and historical fiction, and remains a benchmark "
        "for blockbuster filmmaking."
    ]

    predictions_2 = [
        'James Cameron\'s 1997 epic romantic disaster film "Titanic" tells the '
    ]

    @unittest.skip("Skipping this test case for now due the need of OpenAI API key.")
    def test_GPTScore_helpfulness(self):
        metric = get_metric("generic_bool/relevance")
        result = metric.compute(self.dataset, self.predictions)
        print(result)

        self.assertEqual(result["value"], 1.0)
        self.assertEqual(result["sample_values"], [1.0])

        metric = get_metric("generic_bool/coherence")
        result = metric.compute(self.dataset, self.predictions)
        print(result)

        self.assertEqual(result["value"], 1.0)
        self.assertEqual(result["sample_values"], [1.0])

        metric = get_metric("generic_bool/harmlessness")
        result = metric.compute(self.dataset, self.predictions)
        print(result)

        self.assertEqual(result["value"], 1.0)
        self.assertEqual(result["sample_values"], [1.0])

    @unittest.skip("Skipping this test case for now due the need of OpenAI API key.")
    def test_GPTScore_general_likert(self):
        metric = get_metric("generic_likert/helpfulness")
        result = metric.compute(self.dataset, self.predictions)
        print(result)

        self.assertEqual(result["value"], 5.0)
        self.assertEqual(result["sample_values"], [5.0])

    @unittest.skip("Skipping this test case for now due the need of OpenAI API key.")
    def test_GPTScore_general_pairwise(self):
        metric = get_metric("generic_pairwise/helpfulness")
        result = metric.compare(self.dataset, self.predictions, self.predictions_2)
        print(result)

        self.assertEqual(result["value"], 1.0)
        self.assertEqual(result["sample_values"], [1.0])

    @unittest.skip("Skipping this test case for now due the need of OpenAI API key.")
    def test_GPTScore_general_rank(self):
        metric = get_metric("generic_rank/helpfulness")
        result = metric.rank(
            self.dataset, [[self.predictions[0], self.predictions_2[0]]]
        )
        print(result)

        self.assertEqual(result["value"], "1")
        self.assertEqual(result["sample_values"], ["1"])


if __name__ == "__main__":
    unittest.main()
