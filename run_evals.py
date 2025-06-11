from langfuse import Langfuse
from agent import run_agent
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.models import GeminiModel
import os
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse()

EVAL_MODEL = "gemini-2.0-flash"
API_KEY = os.environ.get("GOOGLE_API_KEY")
eval_model = GeminiModel(model_name=EVAL_MODEL, api_key=API_KEY)

def joyfulness_score(input, output):
      joyfulness_metric = GEval(
            model=eval_model,
            name="Correctness",
            criteria="Determine whether the output is engaging and fun.",
            evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT]
      )
      test_case = LLMTestCase(input=input, actual_output=output)
      joyfulness_metric.measure(test_case)
      return {"score": joyfulness_metric.score, "reason": joyfulness_metric.reason}

def run_experiment(experiment_name, system_prompt):

    dataset = langfuse.get_dataset('evaluation-set')

    for item in dataset.items:
            with item.run(run_name=experiment_name) as trace_id:
                  output = run_agent(item.input["prompt"], system_prompt)

                  eval_result = joyfulness_score(item.input["prompt"], output.content)

                  langfuse.create_score(
                        trace_id=trace_id.trace_id,
                        name="joyfulness score",
                        value=eval_result["score"],
                        comment=eval_result["reason"]
                  )

run_experiment("first_experiment", "Crée une histoire courte (entre 200 et 400 mots), super joyeuse, basée sur le thème qui te va être communiqué par un enfant")