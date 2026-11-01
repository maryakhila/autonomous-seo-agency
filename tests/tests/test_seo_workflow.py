import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from seo_workflow import SEOWorkflow


def test_workflow_has_seven_steps():
    workflow = SEOWorkflow()

    assert len(workflow.workflow) == 7
    assert workflow.workflow[0]["employee"] == "SEO Researcher"
    assert workflow.workflow[-1]["employee"] == "Performance Analyst"
