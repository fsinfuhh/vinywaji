// vim: set filetype=groovy:

pipeline {
    agent {
        kubernetes {
            yaml """
kind: Pod
spec:
  containers:
    - name: podman
      image: quay.io/podman/stable
      tty: true
      securityContext:
        privileged: true
      command:
        - cat
"""
        }
    }
    options {
        skipDefaultCheckout(true)
    }
    stages {
        stage("Checkout SCM") {
            steps {
                checkout scm
            }
        }
        stage("Build Container Image") {
            steps {
                container("podman") {
                    gitStatusWrapper(
                        credentialsId: "github-credentials",
                        description: "Build the container image",
                        failureDescription: "Container image failed to build",
                        successDescription: "Container image was successfully built",
                        gitHubContext: "build-container-image"
                    ) {
                        sh "podman build -t bitbots_drinks ."
                    }
                }
            }
        }
        stage("Upload Container Image") {
            steps {
                container("podman") {
                    gitStatusWrapper(
                        credentialsId: "github-credentials",
                        description: "Upload the container image",
                        failureDescription: "Could not upload the container image",
                        successDescription: "Container image was uploaded",
                        gitHubContext: "upload-container-image"
                    ) {
                        milestone(ordinal: 100)

                        script {
                            withCredentials([usernamePassword(
                                credentialsId: 'github-credentials',
                                passwordVariable: 'registry_password',
                                usernameVariable: 'registry_username'
                            )]) {
                                if (env.TAG_NAME != null) {
                                    // tag events get pushed as the corresponding tag
                                    sh "podman login ghcr.io -u $registry_username -p $registry_password"
                                    sh "podman tag bitbots_drinks ghcr.io/bit-bots/bitbots_drinks:${env.TAG_NAME}"
                                    sh "podman push ghcr.io/bit-bots/bitbots_drinks:${env.TAG_NAME}"
                                }

                                if (env.BRANCH_IS_PRIMARY == "true") {
                                    // commit events get pushed as :dev-latest
                                    sh "podman login ghcr.io -u $registry_username -p $registry_password"
                                    sh "podman tag bitbots_drinks ghcr.io/bit-bots/bitbots_drinks:dev-latest"
                                    sh "podman push ghcr.io/bit-bots/bitbots_drinks:dev-latest"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
