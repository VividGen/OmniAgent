// SPDX-License-Identifier: MIT

pragma solidity 0.8.18;

/// @dev Invalid User Id
error OmniAgentExecutorManager__InValidUserId(uint256 userId);

/// @dev Invalid Executor Id
error OmniAgentExecutorManager__InValidExecutorId(uint256 executorId);

/// @dev No Role To Create Executor
error OmniAgentExecutorManager__NoRoleToCreateExecutor(address sender);
