from lime.lime_text import LimeTextExplainer
import matplotlib.pyplot as plt
import os

from app import bert_predict_proba_preprocessed

class_names = ["LOW", "MEDIUM", "HIGH"]
explainer = LimeTextExplainer(class_names=class_names)

cases = {
    "t1_low": "Hello, I hope you are doing well today.",
    "t4_medium": "You are being really annoying and wasting my time.",
    "t7_high_pass": "clіck hеrе tо clаim yоur frее gіft nоw!!!",
    "t9_high_fail": "Vіsіt thіs secure lоgin pаge nоw: paypaI-alert-center.com",
    "t10_high_fail": "Hеllо frіеnd, 你好, مرحبا, clіck nоw fоr frее mоnеу!!!"
}

output_dir = "06_shap_lime"
os.makedirs(output_dir, exist_ok=True)

for name, text in cases.items():
    print(f"Explaining {name}...")

    exp = explainer.explain_instance(
        text_instance=text,
        classifier_fn=bert_predict_proba_preprocessed,
        num_features=10,
        num_samples=100
    )

    fig = exp.as_pyplot_figure()
    fig.savefig(os.path.join(output_dir, f"{name}_lime.png"), bbox_inches="tight")
    plt.close(fig)

    with open(os.path.join(output_dir, f"{name}_lime.txt"), "w", encoding="utf-8") as f:
        f.write(f"Text: {text}\n")
        f.write(str(exp.as_list()))

print("Done. LIME outputs saved in 06_shap_lime")
