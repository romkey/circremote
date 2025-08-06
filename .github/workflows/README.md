# GitHub Workflows

This directory contains GitHub Actions workflows for the circremote project.

## Available Workflows

### 🔔 PR Notification (`pr-notification.yml`)
**Purpose**: Basic notification when a new PR is submitted
**Triggers**: 
- `pull_request.opened`
- `pull_request.reopened`
- `pull_request.ready_for_review`

**Actions**:
- Notifies @romkey via PR comment
- Automatically assigns @romkey to the PR
- Provides PR details and links

### 🎯 PR Management (`pr-management.yml`)
**Purpose**: Comprehensive PR management and validation
**Triggers**:
- `pull_request.opened`
- `pull_request.reopened`
- `pull_request.ready_for_review`
- `pull_request.synchronize`

**Actions**:
- Detailed notification to @romkey with PR statistics
- Automatic assignment of @romkey
- Smart labeling based on PR content (documentation, bug-fix, enhancement)
- PR validation (description check, external contributor welcome)
- Update notifications when PR is modified

### 🔍 PR Review Request (`pr-review-request.yml`)
**Purpose**: Handle review requests and review submissions
**Triggers**:
- `pull_request_review.submitted`
- `pull_request_review.dismissed`
- `pull_request.review_requested`
- `pull_request.review_request_removed`

**Actions**:
- Notifies @romkey when reviews are requested
- Provides review submission summaries
- Handles review dismissal notifications

## Workflow Features

### Automatic Notifications
All workflows automatically notify @romkey via:
- **PR Comments**: Detailed information about PRs and reviews
- **Automatic Assignment**: @romkey is automatically assigned to new PRs
- **Smart Labeling**: PRs are automatically labeled based on content

### PR Validation
- **Description Check**: Ensures PRs have adequate descriptions
- **External Contributor Welcome**: Special messages for contributors from forks
- **Content Analysis**: Automatically detects documentation, bug fixes, and features

### Review Management
- **Review Request Tracking**: Notifies when reviews are requested
- **Review Summary**: Provides summaries of submitted reviews
- **Review Dismissal**: Tracks when reviews are dismissed

## Workflow Permissions

These workflows require the following permissions:
- `issues: write` - To create comments and manage assignments
- `pull-requests: write` - To add labels and manage PR metadata
- `contents: read` - To read repository contents for analysis

## Customization

### Adding New Triggers
To add new triggers, modify the `on` section of the workflow:

```yaml
on:
  pull_request:
    types: [opened, reopened, ready_for_review, synchronize, closed]
```

### Modifying Notifications
To change notification content, edit the `body` field in the `createComment` calls.

### Adding New Labels
To add new automatic labels, modify the label detection logic in `pr-management.yml`.

## Troubleshooting

### Workflow Not Running
- Check that the workflow files are in the `.github/workflows/` directory
- Verify the workflow syntax is valid YAML
- Ensure the repository has GitHub Actions enabled

### Notifications Not Working
- Verify @romkey has access to the repository
- Check that the workflow has the necessary permissions
- Review the workflow logs for any errors

### Permission Issues
If workflows fail due to permissions, ensure the repository settings allow:
- GitHub Actions to read and write repository contents
- Workflows to create comments and manage issues/PRs

## Maintenance

These workflows are designed to be low-maintenance and self-contained. They use standard GitHub Actions and don't require external dependencies.

To update workflows:
1. Modify the workflow files in this directory
2. Commit and push changes
3. The new workflows will be automatically available for future PRs 