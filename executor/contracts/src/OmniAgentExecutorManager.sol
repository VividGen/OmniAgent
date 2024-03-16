// SPDX-License-Identifier: MIT
pragma solidity 0.8.18;

import "./interfaces/IOmniAgentExecutorManager.sol";
import "./interfaces/IOmniAgentExecutor.sol";
import "./OmniAgentExecutor.sol";
import {
    OmniAgentExecutorManager__InValidUserId,
    OmniAgentExecutorManager__InValidExecutorId,
    OmniAgentExecutorManager__NoRoleToCreateExecutor
} from "./Error.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {Initializable} from "@openzeppelin/contracts/proxy/utils/Initializable.sol";
import {AccessControlEnumerable} from "@openzeppelin/contracts/access/AccessControlEnumerable.sol";

/**
 * @title OmniAgentExecutorManager
 * @notice The OmniAgentExecutorManager contract is used to generate and manage users' executors.
 */
contract OmniAgentExecutorManager is IOmniAgentExecutorManager, Initializable, AccessControlEnumerable {
    using SafeERC20 for IERC20;

    mapping(uint256 => mapping(uint256 => address)) internal _executors;
    uint256 internal _executorIndex;

    // events
    /// @notice Emitted when a executor is created.
    event ExecutorCreated(
        uint256 indexed userId,
        uint256 indexed executorId,
        address indexed executorAddr
    );
    /// @notice Emitted when tokens are deposited.
    event TokensDeposited(address indexed to, uint256 indexed amount, address token);
    /// @notice Emitted when tokens are withdrawn.
    event TokensWithdrawn(
        address indexed from,
        address indexed to,
        uint256 indexed amount,
        address token
    );
    /// @notice Emitted when tokens are transferred.
    event TokensTransferred(
        address indexed from,
        address indexed to,
        uint256 indexed amount,
        address token
    );

    modifier validUserId(uint256 userId) {
        if (userId <= 0) revert OmniAgentExecutorManager__InValidUserId(userId);
        _;
    }

    modifier validExecutorId(uint256 executorId) {
        if (executorId <= 0) revert OmniAgentExecutorManager__InValidExecutorId(executorId);
        _;
    }

    modifier onlyAdmin() {
        if (!hasRole(DEFAULT_ADMIN_ROLE, msg.sender))
            revert OmniAgentExecutorManager__NoRoleToCreateExecutor(msg.sender);
        _;
    }

    constructor() {
        _disableInitializers();
    }

    /// @inheritdoc IOmniAgentExecutorManager
    function initialize(address admin) external override initializer {
        // grants `DEFAULT_ADMIN_ROLE`
        _setupRole(DEFAULT_ADMIN_ROLE, admin);
    }

    /// @inheritdoc IOmniAgentExecutorManager
    // solhint-disable-next-line no-empty-blocks
    function fund() external payable override {}

    /// @inheritdoc IOmniAgentExecutorManager
    function createExecutor(
        uint256 userId
    ) public override validUserId(userId) onlyAdmin returns (uint256 executorId, address executorAddr) {
        IOmniAgentExecutor OmniAgentExecutor = new OmniAgentExecutor();
        executorAddr = address(OmniAgentExecutor);
        _executorIndex++;
        _executors[userId][_executorIndex] = executorAddr;
        executorId = _executorIndex;
        emit ExecutorCreated(userId, _executorIndex, executorAddr);
    }

    /// @inheritdoc IOmniAgentExecutorManager
    function deposit(
        uint256 userId,
        uint256 executorId,
        address token,
        uint256 amount
    ) public override validUserId(userId) validExecutorId(executorId) onlyAdmin {
        address sender = msg.sender;
        address OmniAgentExecutorAddr = _executors[userId][executorId];

        IOmniAgentExecutor OmniAgentExecutor = IOmniAgentExecutor(payable(OmniAgentExecutorAddr));

        IOmniAgentExecutor.Call[] memory calls = new IOmniAgentExecutor.Call[](1);
        if (token != address(0)) {
            calls[0] = IOmniAgentExecutor.Call({
                target: address(token),
                callData: abi.encodeWithSelector(
                    IERC20.transferFrom.selector,
                    sender,
                    OmniAgentExecutorAddr,
                    amount
                )
            });
            OmniAgentExecutor.aggregate(calls);
            emit TokensDeposited(OmniAgentExecutorAddr, amount, token);
        } else {
            OmniAgentExecutor.aggregate{value: amount}(calls);
            emit TokensDeposited(OmniAgentExecutorAddr, amount, address(0));
        }
    }

    /// @inheritdoc IOmniAgentExecutorManager
    function withdraw(
        uint256 userId,
        uint256 executorId,
        address payable to,
        address token,
        uint256 amount
    ) public override validUserId(userId) validExecutorId(executorId) onlyAdmin {
        address OmniAgentExecutorAddr = _executors[userId][executorId];

        IOmniAgentExecutor OmniAgentExecutor = IOmniAgentExecutor(payable(OmniAgentExecutorAddr));

        IOmniAgentExecutor.Call[] memory calls = new IOmniAgentExecutor.Call[](1);
        if (token != address(0)) {
            calls[0] = IOmniAgentExecutor.Call({
                target: address(token),
                callData: abi.encodeWithSelector(IERC20.transfer.selector, to, amount)
            });
            OmniAgentExecutor.aggregate(calls);
            emit TokensWithdrawn(OmniAgentExecutorAddr, to, amount, token);
        } else {
            OmniAgentExecutor.withdraw(to, amount);
            emit TokensWithdrawn(OmniAgentExecutorAddr, to, amount, address(0));
        }
    }

    /// @inheritdoc IOmniAgentExecutorManager
    function transfer(
        uint256 fromUserId,
        uint256 fromExecutorId,
        uint256 toUserId,
        uint256 toExecutorId,
        address token,
        uint256 amount
    )
        public
        override
        validUserId(fromUserId)
        validUserId(toUserId)
        validExecutorId(fromExecutorId)
        validExecutorId(toExecutorId)
        onlyAdmin
    {
        address fromOmniAgentExecutorAddr = _executors[fromUserId][fromExecutorId];
        address toOmniAgentExecutorAddr = _executors[toUserId][toExecutorId];

        IOmniAgentExecutor fromOmniAgentExecutor = IOmniAgentExecutor(payable(fromOmniAgentExecutorAddr));

        IOmniAgentExecutor.Call[] memory calls = new IOmniAgentExecutor.Call[](1);
        if (token != address(0)) {
            calls[0] = IOmniAgentExecutor.Call({
                target: address(token),
                callData: abi.encodeWithSelector(
                    IERC20.transfer.selector,
                    toOmniAgentExecutorAddr,
                    amount
                )
            });

            fromOmniAgentExecutor.aggregate(calls);
            emit TokensTransferred(fromOmniAgentExecutorAddr, toOmniAgentExecutorAddr, amount, token);
        } else {
            fromOmniAgentExecutor.withdraw(payable(toOmniAgentExecutorAddr), amount);
            emit TokensTransferred(fromOmniAgentExecutorAddr, toOmniAgentExecutorAddr, amount, token);
        }
    }

    /// @inheritdoc IOmniAgentExecutorManager
    function getNativeTokenBalance(
        uint256 userId,
        uint256 executorId
    )
        public
        view
        override
        validUserId(userId)
        validExecutorId(executorId)
        returns (uint256 nativeBalance)
    {
        return _executors[userId][executorId].balance;
    }

    /// @inheritdoc IOmniAgentExecutorManager
    function getTokenBalance(
        uint256 userId,
        uint256 executorId,
        address token
    )
        public
        view
        override
        validUserId(userId)
        validExecutorId(executorId)
        returns (uint256 tokenBalance)
    {
        return (IERC20(token).balanceOf(_executors[userId][executorId]));
    }

    /// @inheritdoc IOmniAgentExecutorManager
    function getExecutorAddr(
        uint256 userId,
        uint256 executorId
    ) public view override validUserId(userId) validExecutorId(executorId) returns (address) {
        return _executors[userId][executorId];
    }

    /// @inheritdoc IOmniAgentExecutorManager
    function getExecutorIndex() public view override returns (uint256) {
        return _executorIndex;
    }
}
