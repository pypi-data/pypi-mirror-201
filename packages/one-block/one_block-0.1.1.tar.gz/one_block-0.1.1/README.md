# slack-blocks

`slack-blocks` has started as I needed to start using [Slack's Block Kit](https://api.slack.com/block-kit) for the
design of my application. While there are [a few Python packages available](#alternative-python-implementations)
already, they were either using a license I was uncomfortable with, or have simply not been kept up-to-date.

> Note, this is still a pre-release version, and as such, features might change or go away entirely.

## Available features

While this is an on-going effort, this was initially driven by the fact I needed something to be able to move quickly.
As such, it's implementing all the existing blocks, but some things might not be available, e.g. specifying `block_ids`.
Documentation is also non-existent, but something I plan on adding as soon as possible.

It is meant to be fairly simple to use, with re-usability at the forefront of its design.

## Roadmap

- [x] Support for all blocks
- [ ] Documentation
- [ ] Python package publishing
- [ ] Tests
- [ ] Type annotations

## Appendix

### Alternative Python Implementations

[ASU-CodeDevils/slack-blockkit](https://github.com/ASU-CodeDevils/slack-blockkit) - Did not seem to be well maintained
[NickLambourne/slackblocks](https://github.com/nicklambourne/slackblocks) - BSD licensed and maintenance queries