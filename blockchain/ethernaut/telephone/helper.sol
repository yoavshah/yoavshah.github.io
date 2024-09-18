// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "./TestContract.sol";

contract TestContractHelper {
    TestContract public testContract;

    constructor(address counterAddress) {
        testContract = TestContract(counterAddress);

        testContract.changeOwner(msg.sender);
    }
}