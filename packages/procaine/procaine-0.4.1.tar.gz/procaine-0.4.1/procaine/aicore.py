# Procaine is a REST client library for AI Core.
# Copyright (C) 2022 Roman Kindruk

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import json
import base64
import posixpath
import os
import re
import requests
import time
from urllib.parse import urljoin, urlparse
from authlib.integrations.requests_client import OAuth2Session


def getid(obj):
    if isinstance(obj, dict):
        return obj["id"]
    return obj


class Client:
    """Initializes the connection to AI Core and obtains a Bearer token.

    :param ai_api_url: A URL to the AI API instance.
    :param auth: Dictionary with creadentials to obtain a Bearer token.
        Should have ``url``, ``clientid`` and ``clientsecret`` keys.
    :param rg: (optional) A name of a ``resource group`` to use with every call.

    Usage::

      >>> from procaine import aicore

      >>> auth = dict(url=AUTH_URL, clientid=CLIENT_ID, clientsecret=CLIENT_SECRET)
      >>> api = aicore.Client(AI_API_URL, auth)

      >>> api.healthz()
      {'message': 'OK', 'status': 'READY'}
    """

    def __init__(self, ai_api_url, auth, rg="default"):
        self.url = ai_api_url
        self.rg = rg
        self.authurl = urlparse(auth["url"]).netloc

        r = OAuth2Session(auth["clientid"], auth["clientsecret"]).fetch_token(
            auth["url"] + "/oauth/token"
        )
        self.sess = requests.Session()
        self.sess.headers.update(
            {
                "Authorization": "Bearer %s" % r["access_token"],
                "Content-Type": "application/json",
                "AI-Resource-Group": self.rg,
            }
        )
        self.sess.hooks = {"response": lambda r, *args, **kwargs: r.raise_for_status()}

    def __repr__(self):
        client, _, _ = self.authurl.partition(".")
        return f"<AICore client='{client}' api='{self.url}' rg='{self.rg}'>"

    def healthz(self):
        """
        Checks AI API service status.
        """
        return self.sess.get(urljoin(self.url, "/v2/lm/healthz")).json()

    def meta(self):
        """
        Returns AI API service metadata.
        """
        return self.sess.get(urljoin(self.url, "/v2/lm/meta")).json()

    def kpi(self):
        """
        Provides usage statistics.
        """
        return self.sess.get(urljoin(self.url, "/v2/analytics/kpis")).json()

    def list_s3_secrets(self):
        """
        Lists registered S3 secrets.
        """
        return self.sess.get(urljoin(self.url, "/v2/admin/objectStoreSecrets")).json()[
            "resources"
        ]

    def create_s3_secret(
        self,
        name,
        access_key_id,
        secret_access_key,
        bucket=None,
        prefix=None,
        endpoint=None,
        region=None,
    ):
        """
        Registers credentials to access S3 bucket.

        :param name: The name of a secret.
        :param access_key_id: Access key ID to access the bucket.
        :param secret_access_key: Secret access key to access the bucket.
        :param bucket: (optional) A bucket name.
        :param prefix: (optional) A key name prefix.
        :param endpoint: (optional) S3 service endpoint.
        :param region: (optional) A region of the bucket.
        """

        data = {
            "name": name,
            "type": "S3",
            "data": {
                "AWS_ACCESS_KEY_ID": access_key_id,
                "AWS_SECRET_ACCESS_KEY": secret_access_key,
            },
        }
        if bucket:
            data["bucket"] = bucket
        if endpoint:
            data["endpoint"] = endpoint
        if prefix:
            data["pathPrefix"] = prefix
        if region:
            data["region"] = region
        return self.sess.post(
            urljoin(self.url, "/v2/admin/objectStoreSecrets"), json=data
        ).json()

    def delete_s3_secret(self, name):
        """
        Deletes an object-store secret.
        """
        return self.sess.delete(
            urljoin(self.url, f"/v2/admin/objectStoreSecrets/{name}")
        ).json()

    def list_docker_registry_secrets(self):
        """
        Lists registered docker registry secrets.
        """
        return self.sess.get(
            urljoin(self.url, "/v2/admin/dockerRegistrySecrets")
        ).json()["resources"]

    def create_docker_registry_secret(self, name, registry, username, password):
        """
        Registers credentials to access a docker registry.

        :param name: The name of a secret.
        :param registry: A docker registry address.
        :param username: Username to access the registry.
        :param password: Password to access the registry.
        """

        secret = {
            "name": name,
            "data": {
                ".dockerconfigjson": json.dumps(
                    {
                        "auths": {
                            registry: {
                                "username": username,
                                "password": password,
                            }
                        }
                    }
                )
            },
        }
        return self.sess.post(
            urljoin(self.url, "/v2/admin/dockerRegistrySecrets"), json=secret
        ).json()

    def delete_docker_registry_secret(self, name):
        """
        Deletes a docker registry secret.
        """
        return self.sess.delete(
            urljoin(self.url, f"/v2/admin/dockerRegistrySecrets/{name}")
        ).json()

    def list_generic_secrets(self):
        """
        Lists registered generic secrets.
        """
        return self.sess.get(urljoin(self.url, f"/v2/admin/secrets")).json()[
            "resources"
        ]

    def create_generic_secret(self, name, data):
        """
        Creates a generic secret.

        :param name: The name of a secret.
        :param data: Dict of ``key`` -> ``value``.
        """
        secret = {
            "name": name,
            "data": {
                k: base64.b64encode(v.encode("ascii")).decode("ascii")
                for k, v in data.items()
            },
        }
        return self.sess.post(
            urljoin(self.url, f"/v2/admin/secrets"), json=secret
        ).json()

    def delete_generic_secret(self, name):
        """
        Deletes a generic secret.
        """
        return self.sess.delete(urljoin(self.url, f"/v2/admin/secrets/{name}")).json()

    def list_git_repositories(self):
        """
        Lists registered git repositories.
        """
        return self.sess.get(urljoin(self.url, "/v2/admin/repositories")).json()[
            "resources"
        ]

    def create_git_repository(self, name, url, username=None, password=None):
        """
        Registers credentials to access a git repository.

        :param name: The name of a secret.
        :param url: A URL to the git repository.
        :param username: (optional) Username to access the registry.
        :param password: (optional) Password to access the registry.
        """

        repo = {
            "name": name,
            "url": url,
            "username": username,
            "password": password,
        }
        return self.sess.post(
            urljoin(self.url, "/v2/admin/repositories"), json=repo
        ).json()

    def delete_git_repository(self, name):
        """
        Deletes a git repository secret.
        """
        return self.sess.delete(
            urljoin(self.url, f"/v2/admin/repositories/{name}")
        ).json()

    def list_applications(self):
        """Lists created sync applications."""
        return self.sess.get(urljoin(self.url, "/v2/admin/applications")).json()[
            "resources"
        ]

    def application(self, app):
        """Returns application details.

        :param app: Application object, name or ID
        """
        if not isinstance(app, dict):
            app = self.sess.get(
                urljoin(self.url, f"/v2/admin/applications/{app}")
            ).json()
        return {**app, **self._application_status(app)}

    def _application_status(self, app):
        """Returns a sync status of the application.

        :param app: Application object
        """
        return self.sess.get(
            urljoin(self.url, f"/v2/admin/applications/{app['applicationName']}/status")
        ).json()

    def create_application(self, repo_name, path=".", ref="HEAD"):
        """Creates an application to sync git repository with AI Core.

        :param repo_name: Name of a registered git repository.
        :param path: (optional) Directory in a repo to sync.
        :param ref: (optional) Git reference, i.e. branch, tag, etc.
        """
        name = repo_name
        if path and path != ".":
            s = re.sub("[^0-9a-zA-Z]+", "-", path.strip("/"))
            name = f"{name}-{s}"
        app = {
            "applicationName": name,
            "repositoryName": repo_name,
            "revision": ref,
            "path": path,
        }
        return self.sess.post(
            urljoin(self.url, "/v2/admin/applications"), json=app
        ).json()

    def delete_application(self, name):
        """Deletes an application."""
        return self.sess.delete(
            urljoin(self.url, f"/v2/admin/applications/{name}")
        ).json()

    def list_resource_groups(self):
        """Lists resource groups."""
        return self.sess.get(urljoin(self.url, "/v2/admin/resourceGroups")).json()[
            "resources"
        ]

    def create_resource_group(self, name):
        """Creates a resource group."""
        rg = {"resourceGroupId": name}
        return self.sess.post(
            urljoin(self.url, "/v2/admin/resourceGroups"), json=rg
        ).json()

    def list_scenarios(self):
        """Lists available scenarios."""
        return self.sess.get(urljoin(self.url, "/v2/lm/scenarios")).json()["resources"]

    def list_templates(self, scenario=None):
        """Lists templates (executables).

        :param scenario: (optional) Scenario object or ID.  Returns only templates belong to the scenario.
        """

        def get_executables(scenario_id):
            url = urljoin(self.url, f"/v2/lm/scenarios/{scenario_id}/executables")
            return self.sess.get(url).json()["resources"]

        scenario_id = getid(scenario)
        if scenario_id:
            return get_executables(scenario_id)
        return [t for s in self.list_scenarios() for t in get_executables(s["id"])]

    def template(self, name, scenario=None):
        """Returns information about a template.

        :param name: Name of the template (executable ID).
        :param scenario: (optional) Scenario object or ID.
        """

        def get_executable(scenario_id, executable_id):
            url = urljoin(
                self.url, f"/v2/lm/scenarios/{scenario_id}/executables/{executable_id}"
            )
            return self.sess.get(url).json()

        scenario_id = getid(scenario)
        if scenario_id:
            return get_executable(scenario_id, name)

        for s in self.list_scenarios():
            try:
                return get_executable(s["id"], name)
            except requests.HTTPError as err:
                if err.response.status_code == 404:
                    continue
                raise
        return None

    def list_executions(self):
        """Returns all executions."""
        return self.sess.get(urljoin(self.url, f"/v2/lm/executions")).json()[
            "resources"
        ]

    def _create_configuration(self, name, executable, parameters=None, artifacts=None):
        conf = {
            "name": name,
            "executableId": executable["id"],
            "scenarioId": executable["scenarioId"],
        }
        if parameters:
            bindings = [{"key": k, "value": v} for k, v in parameters.items()]
            conf["parameterBindings"] = bindings
        if artifacts:
            bindings = [
                {
                    "key": binding,
                    "artifactId": getid(artifact),
                }
                for binding, artifact in artifacts.items()
            ]
            conf["inputArtifactBindings"] = bindings
        return self.sess.post(
            urljoin(self.url, "/v2/lm/configurations"), json=conf
        ).json()

    def _configuration(self, id):
        return self.sess.get(urljoin(self.url, f"/v2/lm/configurations/{id}")).json()

    def create_execution(self, template, parameters=None, artifacts=None):
        """Starts a workflow execution.

        :param template: Template name or object returned from :meth:`Client.template` or :meth:`Client.list_templates`.
        :param parameters: (optional) Dict of ``param-name`` -> ``value``.
        :param artifacts: (optional) Dict of ``binding-name`` -> ``S3 object URL or artifact or artifact ID``.
        """

        def make_artifact(obj, template):
            if isinstance(obj, str) and obj.startswith("s3://"):
                return self.create_artifact(
                    obj, "dataset", template["scenarioId"], name=os.path.basename(obj)
                )
            return obj

        if isinstance(template, str):
            tmpl = self.template(template)
            if tmpl is None:
                raise ValueError(f"Can't find the template '{template}'")
            template = tmpl

        if artifacts:
            artifacts = {k: make_artifact(v, template) for k, v in artifacts.items()}

        cfg = self._create_configuration(
            template["id"], template, parameters, artifacts
        )
        return self.sess.post(
            urljoin(self.url, "/v2/lm/executions"), json={"configurationId": cfg["id"]}
        ).json()

    def stop_execution(self, execution):
        """Stops a running flow.

        :param execution: Execution object or ID.
        """
        return self.sess.patch(
            urljoin(self.url, f"/v2/lm/executions/{getid(execution)}"),
            json={"targetStatus": "STOPPED"},
        ).json()

    def delete_execution(self, execution):
        """Deletes a flow.

        :param execution: Execution object or ID.
        """
        return self.sess.delete(
            urljoin(self.url, f"/v2/lm/executions/{getid(execution)}")
        ).json()

    def execution(self, execution):
        """Shows an execution status.

        :param execution: Execution object or ID.
        """
        return self.sess.get(
            urljoin(self.url, f"/v2/lm/executions/{getid(execution)}")
        ).json()

    def execution_logs(self, execution):
        """Shows pods' logs of an execution.

        :param execution: Execution object or ID.
        """
        logs = self.sess.get(
            urljoin(self.url, f"/v2/lm/executions/{getid(execution)}/logs")
        ).json()
        return "\n".join(
            [x["msg"] for x in logs["data"]["result"] if x["container"] == "main"]
        )

    def create_artifact(self, url, kind, scenario, name, description=""):
        """Registers an artifact.

        :param url: Object's URL.
        :param kind: One of the: ``model``, ``dataset``, ``resultset`` or ``other``.
        :param scenario: Scenario object or ID.
        :param name: Name of an artifact.
        :param description: (optional) Artifact's description.
        """
        if not url.startswith("ai://"):
            for secret in self.list_s3_secrets():
                meta = secret["metadata"]
                path = "s3://" + posixpath.join(
                    meta["storage.ai.sap.com/bucket"],
                    meta["storage.ai.sap.com/pathPrefix"],
                )
                if url.startswith(path):
                    url = url.replace(path.rstrip("/"), "ai://" + secret["name"])
                    break
        a = {
            "url": url,
            "name": name,
            "scenarioId": getid(scenario),
            "kind": kind,
            "description": description,
        }
        return self.sess.post(urljoin(self.url, "/v2/lm/artifacts"), json=a).json()

    def list_artifacts(self):
        """Lists all registered artifacts."""
        return self.sess.get(urljoin(self.url, "/v2/lm/artifacts")).json()["resources"]

    def artifact(self, id):
        """Returns artifact by ID."""
        return self.sess.get(urljoin(self.url, f"/v2/lm/artifacts/{id}")).json()

    def list_deployments(self):
        """Returns all deployments."""
        return self.sess.get(urljoin(self.url, f"/v2/lm/deployments")).json()[
            "resources"
        ]

    def create_deployment(self, template):
        """Starts an inference server.

        :param template: Template name or object returned from :meth:`Client.template` or :meth:`Client.list_templates`.
        """

        if isinstance(template, str):
            tmpl = self.template(template)
            if tmpl is None:
                raise ValueError(f"Can't find the template '{template}'")
            template = tmpl

        cfg = self._create_configuration(template["id"], template)

        return self.sess.post(
            urljoin(self.url, "/v2/lm/deployments"), json={"configurationId": cfg["id"]}
        ).json()

    def deployment(self, deployment):
        """Shows a deployment status.

        :param deployment: Deployment object or ID.
        """
        return self.sess.get(
            urljoin(self.url, f"/v2/lm/deployments/{getid(deployment)}")
        ).json()

    def deployment_logs(self, deployment):
        """Shows pods' logs of a deployment.

        :param deployment: Deployment object or ID.
        """
        logs = self.sess.get(
            urljoin(self.url, f"/v2/lm/deployments/{getid(deployment)}/logs")
        ).json()
        return "\n".join([x["msg"] for x in logs["data"]["result"]])

    def stop_deployment(self, deployment):
        """Stops a model server.

        :param deployment: Deployment object or ID.
        """
        return self.sess.patch(
            urljoin(self.url, f"/v2/lm/deployments/{getid(deployment)}"),
            json={"targetStatus": "STOPPED"},
        ).json()

    def _wait_deployment_status(self, deployment, status):
        # poll a deployment every 5 sec. until deployment turn to 'status'.
        # break after ~1 minute.
        TIMEOUT = 60  # sec.
        PERIOD = 5  # sec.
        for i in range(TIMEOUT // PERIOD):
            if self.deployment(deployment)["status"] == status:
                break
            time.sleep(PERIOD)

    def delete_deployment(self, deployment):
        """Deletes a model server.

        :param deployment: Deployment object or ID.
        """
        if isinstance(deployment, str):
            deployment = self.deployment(deployment)
        if deployment["status"] == "RUNNING":
            self.stop_deployment(deployment)
            self._wait_deployment_status(deployment, "STOPPED")
        return self.sess.delete(
            urljoin(self.url, f"/v2/lm/deployments/{deployment['id']}")
        ).json()

    def predict(self, deployment, path="", data=None):
        """Sends HTTP request to a model server.

        :param deployment: Deployment object or ID.
        :param path: (optional) Path attached to a deployment URL.
        :param data: (optional) Data to be passed with a request.
            Sends a GET request when empty.
        """

        if isinstance(deployment, str) or deployment["status"] != "RUNNING":
            deployment = self.deployment(deployment)

        if deployment["status"] != "RUNNING":
            raise ValueError(f"Deployment status is '{deployment['status']}'")

        url = urljoin(deployment["deploymentUrl"] + "/", path.lstrip("/"))
        if data:
            return self.sess.post(url, json=data).json()
        return self.sess.get(url).json()
