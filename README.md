# Ontology Pipeline exploration 01: Tic-tac-toe

## Purpose

An independent learning experiment exploring Jessica Talisman's [Ontology Pipeline](https://jesstalisman-ia.github.io/ontology-pipeline/) using a small, familiar and independently verifiable domain. The goal is to learn about the modelling method, not to build a game.

## Initial scope

Conventional 3×3 tic-tac-toe, two players, alternating turns, X starts. Variants, strategy, user interfaces and implementation choices are initially out of scope.

## First competency question (proposed)

Given a reachable game position, which squares may the next player legally mark?

## Hypothesis

An explicit domain model can distinguish an empty square from a legal destination, including when a game has already ended.

## Independent checks

- An empty initial board permits nine destinations.
- An occupied square is not a legal destination.
- A reachable position with a winning line permits no further moves, even if empty squares remain.
- A full drawn board permits no further moves.

These are proposed checks, not executed results. Later experiments may explore exhaustive reachable-state verification.

## Working approach

Review the source methodology before each modelling increment. Record source evidence, interpretation, decisions, artefacts, predictions, counterexamples and observations. Work incrementally, review and commit meaningful steps. Avoid premature generalisation or assumptions about required implementation technology.

## Related work

- [Modelling a modelling method](https://github.com/scsyme/modelling-a-modelling-method): separate exploration of the pipeline itself.
- [Candidate experiment backlog](https://github.com/scsyme/modelling-a-modelling-method/blob/main/_meta/experiment-backlog.md): provisional ideas, not a committed roadmap.

## Status

Initial experimental framing, awaiting review. No ontology or executable model has yet been created.
