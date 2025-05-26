// NuN Token Smart Contract
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract NuNToken {
    string public name = "NuN Token";
    string public symbol = "NUN";
    uint8 public decimals = 18;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;

    constructor(address founder) {
        totalSupply = 100_000_000 * (10 ** uint256(decimals));
        balanceOf[founder] = (totalSupply * 51) / 100;
        balanceOf[address(this)] = totalSupply - balanceOf[founder];
    }
}
