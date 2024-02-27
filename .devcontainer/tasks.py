from textwrap import dedent
from invoke import task, Context
import os
import json

KUBE_VERSION = os.getenv("KUBE_VERSION", "1.27")
CLUSTER_NAME = os.getenv("CLUSTER_NAME", "elyra-kfp")
CLUSTER_PRODUCT = os.getenv("CLUSTER_PRODUCT", "kind")


@task()
def create_cluster(
    ctx: Context,
    cluster_name=CLUSTER_NAME,
    product=CLUSTER_PRODUCT,
    kube_version=KUBE_VERSION,
):
    """Creates a development cluster using ctlplt and kind"""
    cluster_name = f"{product}-{cluster_name}"
    clusters = ctx.run(
        dedent(
            """
        ctlptl  get cluster -o json | jq '.items[] | select(.kind == "Cluster") | .name'
        """
        ),
        hide=True,
    ).stdout.splitlines()
    clusters = [json.loads(line) for line in clusters]
    if cluster_name in clusters:
        print(f"Cluster {cluster_name} alredy exists")
        return
    ctx.run(
        f"ctlptl create cluster {product} --name {cluster_name} "
        f"--registry kind-registry --kubernetes-version {kube_version}",
        pty=True,
    )


@task()
def delete_cluster(ctx: Context, cluster_name=CLUSTER_NAME, product=CLUSTER_PRODUCT):
    """Deltes the cluster"""
    cluster_name = f"{product}-{cluster_name}"
    ctx.run(f"ctlptl delete cluster {cluster_name}", warn=True)
