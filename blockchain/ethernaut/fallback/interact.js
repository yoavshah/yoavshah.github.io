const { ethers } = require("hardhat");

// npx hardhat console --network localhost
// npx hardhat run --network localhost scripts/interact.js
async function main () {
    const address = '0x5FbDB2315678afecb367f032d93F642f64180aa3';
    const TestContract = await ethers.getContractFactory('TestContract');
    const testContract = TestContract.attach(address);

    const [owner, addr1, addr2] = await ethers.getSigners();

    old_owner = await testContract.owner();
    console.log(old_owner)
    
    old_balance = await ethers.provider.getBalance(await testContract.getAddress())
    console.log(old_balance)

    contribute_result = await testContract.connect(addr1).contribute({
        value: 1
    });

    // console.log(contribute_result);

    const tx = {
        to: address,
        value: ethers.parseEther("0.01"),
    };

    const transactionResponse = await addr1.sendTransaction(tx);
    // console.log(transactionResponse);

    newOwner = await testContract.owner();
    console.log(newOwner)

    withdraw_result = await testContract.connect(addr1).withdraw();
    // console.log(withdraw_result);

    current_balance = await ethers.provider.getBalance(await testContract.getAddress())
    console.log(current_balance)
}



main()
.then(() => process.exit(0))
.catch(error => {
    console.error(error);
    process.exit(1);
});