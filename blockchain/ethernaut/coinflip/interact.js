const { ethers } = require("hardhat");

// npx hardhat console --network localhost
// npx hardhat run --network localhost scripts/interact.js
async function main () {
    const address = '0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512';
    const TestContract = await ethers.getContractFactory('TestContract');
    const testContract = TestContract.attach(address);

    const [owner, addr1, addr2] = await ethers.getSigners();

    FACTOR = BigInt("57896044618658097711785492504343953926634992332820282019728792003956564819968")

    currentConsecutiveWins = await testContract.consecutiveWins();
    console.log(currentConsecutiveWins)

    for (let i = 0; i < 10; i++) 
    {
        currentBlockNumber = await ethers.provider.getBlockNumber();
        currentBlock = await ethers.provider.getBlock(currentBlockNumber);

        blockHash = currentBlock.hash;

        blockHashInt = BigInt(blockHash)

        coinFlip = blockHashInt / FACTOR

        side = coinFlip == 1 ? true : false;


        flipResult = await testContract.flip(side)
        console.log("Current size is " + side + " - success = " + flipResult);


        currentConsecutiveWins = await testContract.consecutiveWins();
        console.log(currentConsecutiveWins)
    }


}



main()
.then(() => process.exit(0))
.catch(error => {
    console.error(error);
    process.exit(1);
});