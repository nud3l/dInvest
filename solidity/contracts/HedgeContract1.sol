pragma solidity ^0.4.0;

contract HedgeContract1 {
  struct Investment {
    address investor;
    uint value;
    uint nowValue;
    uint period;
    uint withdrawalLimit;
  }

  address public creator;
  address public investAgent;
  address public buyAgent;
  uint public minimumInvestment;

  mapping(address => Investment) public investments;

  // Events - publicize actions to external listeners
  event InvestmentOfferByBot(address accountAddress, uint amount);
  event NewInvestmentByUser(address accountAddress, uint amount);

  // Helper function to guard functions
  modifier onlyBy(address _account)
  {
    if (msg.sender != _account)
        throw;
    _;
  }

  function HedgeContract1(
      uint _minimumInvestment,
      address _investAgent,
      address _buyAgent
    ) {
      // Set contract creator when creating the contract
      creator = msg.sender;
  }

  // Set new invest agent - only owner
  function setInvestAgent(address newInvestAgent)
    onlyBy(creator)
  {
    investAgent = newInvestAgent;
  }

  // Set new buy agent - only owner
  function setBuyAgent(address newBuyAgent)
    onlyBy(creator)
  {
    buyAgent = newBuyAgent;
  }

  // Set new minimum investment - only owner
  function setMinimumInvestment(uint newMinimumInvestment)
    onlyBy(creator)
  {
    // TODO - If its the same do not update
    minimumInvestment = newMinimumInvestment;
  }

  // Create a new investment
  function createInvestment() payable {
    if (msg.value < minimumInvestment) {
      throw;
    }

    // TODO - existing investment?
    // 3, 1 to change
    investments[msg.sender] = Investment(msg.sender, msg.value, msg.value, 3, 1);

    // Publish event
    NewInvestmentByUser(msg.sender, msg.value);
  }

  // Investment opportunity - only agent
  // For testing invest agent decide to invest or not
  function investOffer(address account, uint amount, bool invest)
    onlyBy(investAgent)
  {
    // TODO - implement criteria here

    if (invest) {
      InvestmentOfferByBot(account, amount); // fire event
    } else {
      throw;
    }
  }

  // After investment buy agent calls this
  function afterInvestOffer(address account, uint amount)
    onlyBy(buyAgent)
  {
    investments[account].nowValue = amount;
  }

  // Withdrawal by user
  function withdrawalUser(uint withdrawAmount) public returns (bool)
  {
      if (investments[msg.sender].nowValue >= withdrawAmount && withdrawAmount < investments[msg.sender].withdrawalLimit) {
        // Reduce balance before sending
        investments[msg.sender].nowValue -= withdrawAmount;

        if(!msg.sender.send(withdrawAmount)) {
          // Failed send
          investments[msg.sender].nowValue += withdrawAmount;
          return false;
        }

        return true;
      }

      return false;
  }

  // Kill the contract and send the funds to creator
  // TODO - This has to be improved - send funds according to nowValue back to investors
  function kill() {
    if (msg.sender == creator) suicide(creator);
  }

  // Get investment details from investments mapping
  function getInvestmentCurrentValue(address investor) constant
    returns(uint nowValue)
  {
    nowValue = investments[investor].nowValue;
  }
}
