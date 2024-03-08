Twelve Labs appreciates your interest in contributing to this repository. By participating, you can help us improve the SDK and make it even better.

# Getting Started

To begin contributing, follow the steps below:

1. Fork the repository to your GitHub account

2. Clone the forked repository to your local machine.

	```shell
	git clone https://github.com/your-username/twelvelabs-python.git
	```

3. Create a new branch for your changes:

	```shell
	git checkout -b feature/your-feature
	```

4. Make your changes or additions to the codebase.

5. Commit your changes with a descriptive message, and use the `-s` flag to sign your commit:

	```shell
	git commit -m "Your commit message" -s
	```

6. Push the changes to your forked repository:

	```shell
	git push origin feature/your-feature
	```

7. Open a pull request from your forked repository to the main repository.

# Pull Request Guidelines

To contribute your changes, please follow these guidelines for submitting a pull request:

- Ensure that your branch is up to date with the latest changes from the main repository.

	```shell
	git fetch upstream
	git merge upstream/main
	```

- Resolve any conflicts that arise during the merge process.
- Run the necessary tests to ensure that your changes do not introduce any new issues.
- Provide a clear and descriptive title for your pull request.
- Include a detailed description of the changes you made and why they are necessary.
- Reference any related issues in your pull request using the appropriate GitHub syntax.
- Request reviewers for your pull request, and be open to feedback and suggestions.


# Contributing and Issue Tracking

We welcome your contributions and value your feedback for our SDK. If you encounter any issues, have feature requests, questions, or suggestions, we encourage you to use the [GitHub Issues](https://github.com/twelvelabs-io/twelvelabs-python/issues) page to communicate with us. Please follow the guidelines below when filing different types of issues.

## Bug Reports

If you discover a bug, an error, or any unexpected behavior while using the SDK, please help us by submitting a bug report. To file a bug report, follow these steps:

1. On the [Issues](https://github.com/twelvelabs-io/twelvelabs-python/issues) page, check that a similar issue does not already exist, and select the **New Issue** button.
2. Provide a descriptive title for the issue that summarizes the problem.
3. In the issue description, include the following details:
	- Steps to reproduce the issue.
	- Expected behavior.
	- Actual behavior experienced.
	- Any relevant screenshots, error messages or stack traces.
5. Assign the `bug` label to the issue.
6. Submit the issue.

# Feature Requests

If you have a feature or enhancement suggestion for the SDK, please submit a feature request. To file a feature request, follow these steps:

1. On the [Issues](https://github.com/twelvelabs-io/twelvelabs-python/issues) page, check that a similar issue does not already exist, and select the **New Issue** button.
2. Provide a concise and clear title that describes the requested feature.
3. In the issue description, explain the rationale behind the feature request and any additional details that can help us understand your needs better.
4. Assign the `enhancement` label to the issue.
5. Submit the issue.

# Questions and Support
If you have a question about using the SDK or need support, we are here to assist you. To ask a question or request support, follow these steps:

1. On the [Issues](https://github.com/twelvelabs-io/twelvelabs-python/issues) page, check that a similar issue does not already exist, and select the **New Issue** button.
2. Provide a clear and concise title that summarizes your question or support request.
3. In the issue description, ask your question or describe the support you require.
4. Assign the `question` label to the issue.
5. Submit the issue.

# Other Issues

If you have any other types of issues, such as documentation improvements, suggestions, or general feedback, please feel free to submit them as well. Please review the available tags in our issue tracker and choose the most appropriate tag that matches your issue.

We appreciate your collaboration in properly tagging and categorizing issues. By doing so, we can effectively manage and address them, leading to a better experience for everyone. Thank you for your contribution!

# License 

We use the Developer Certificate of Origin (DCO) in lieu of a Contributor License Agreement for all contributions to Twelve Labs' open-source projects. We request that contributors agree to the terms of the DCO and indicate that agreement by signing all commits made to Twelve Labs' projects by adding a line with your name and email address to every Git commit message contributed, as shown in the example below:

```
Signed-off-by: Jane Doe <jane.doe@example.com>
```

You can sign your commit automatically with Git by using `git commit -s` if you have your `user.name` and `user.email` set as part of your Git configuration.
We ask that you use your real name (please, no anonymous contributions or pseudonyms). By signing your commitment, you are certifying that you have the right have the right to submit it under the open-source license used by that particular project. You must use your real name (no pseudonyms or anonymous contributions are allowed.)
We use the Probot DCO GitHub app to check for DCO signoffs of every commit.
If you forget to sign your commits, the DCO bot will remind you and give you detailed instructions for how to amend your commits to add a signature.
