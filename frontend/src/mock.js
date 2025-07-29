// Mock data for Monopoly game - this will be replaced with backend API calls later

export const mockGameData = {
  properties: [
    // GO and Special Spaces
    { id: 1, name: "GO", type: "special", color: "bg-green-600", price: null, rent: null, owner: null },
    
    // Brown Properties
    { id: 2, name: "Baltic Ave", type: "property", color: "bg-amber-800", price: 60, rent: 4, owner: null, description: "Affordable starter property" },
    { id: 3, name: "Reading Railroad", type: "railroad", color: "bg-gray-700", price: 200, rent: 25, owner: null, description: "Major transportation hub" },
    
    // Light Blue Properties  
    { id: 4, name: "Oriental Ave", type: "property", color: "bg-cyan-500", price: 100, rent: 6, owner: null, description: "Growing neighborhood" },
    { id: 5, name: "Vermont Ave", type: "property", color: "bg-cyan-500", price: 100, rent: 6, owner: null, description: "Quiet residential area" },
    
    // Special Space
    { id: 6, name: "Jail", type: "special", color: "bg-red-600", price: null, rent: null, owner: null },
    
    // Pink Properties
    { id: 7, name: "St. Charles", type: "property", color: "bg-pink-500", price: 140, rent: 10, owner: null, description: "Historic district" },
    { id: 8, name: "Electric Co", type: "utility", color: "bg-yellow-500", price: 150, rent: 15, owner: null, description: "Power utility company" },
    { id: 9, name: "States Ave", type: "property", color: "bg-pink-500", price: 140, rent: 10, owner: null, description: "Commercial center" },
    
    // Orange Properties
    { id: 10, name: "Tennessee", type: "property", color: "bg-orange-500", price: 180, rent: 14, owner: null, description: "Popular destination" },
    
    // Special Space  
    { id: 11, name: "Free Parking", type: "special", color: "bg-blue-600", price: null, rent: null, owner: null },
    
    // Red Properties
    { id: 12, name: "Kentucky Ave", type: "property", color: "bg-red-600", price: 220, rent: 18, owner: null, description: "Prime real estate" },
    { id: 13, name: "Indiana Ave", type: "property", color: "bg-red-600", price: 220, rent: 18, owner: null, description: "High-value district" },
    
    // Yellow Properties
    { id: 14, name: "Atlantic Ave", type: "property", color: "bg-yellow-500", price: 260, rent: 22, owner: null, description: "Luxury avenue" },
    { id: 15, name: "Ventnor Ave", type: "property", color: "bg-yellow-500", price: 260, rent: 22, owner: null, description: "Upscale neighborhood" },
    
    // Special Space
    { id: 16, name: "Go to Jail", type: "special", color: "bg-red-700", price: null, rent: null, owner: null },
    
    // Green Properties
    { id: 17, name: "Pacific Ave", type: "property", color: "bg-green-600", price: 300, rent: 26, owner: null, description: "Premium location" },
    { id: 18, name: "Water Works", type: "utility", color: "bg-blue-500", price: 150, rent: 15, owner: null, description: "Water utility company" },
    
    // Dark Blue Properties (Most Expensive)
    { id: 19, name: "Park Place", type: "property", color: "bg-blue-900", price: 350, rent: 35, owner: null, description: "Ultra-luxury property" },
    { id: 20, name: "Boardwalk", type: "property", color: "bg-blue-900", price: 400, rent: 50, owner: null, description: "Most prestigious address" }
  ],

  initialGameState: {
    players: [
      {
        id: 1,
        name: "You",
        money: 1500,
        position: 0,
        properties: [],
        isBot: false,
        difficulty: null
      },
      {
        id: 2,
        name: "Slowpoke Sam",
        money: 1500,
        position: 0,
        properties: [],
        isBot: true,
        difficulty: "Mentally slow"
      },
      {
        id: 3,
        name: "Moderate Mike",
        money: 1500,
        position: 0,
        properties: [],
        isBot: true,
        difficulty: "Medium rare"
      },
      {
        id: 4,
        name: "Strategic Sarah",
        money: 1500,
        position: 0,
        properties: [],
        isBot: true,
        difficulty: "Highly proficient"
      }
    ],
    currentPlayerIndex: 0,
    gamePhase: "playing", // playing, ended
    winner: null
  }
};

// Bot AI Decision Engine - simulates different difficulty levels
export const botDecisionEngine = (bot, property) => {
  const affordability = bot.money / property.price;
  const rentRatio = property.rent / property.price;
  
  switch (bot.difficulty) {
    case "Mentally slow":
      // Simple decision: buy if affordable and cheap
      if (affordability > 3 && property.price < 150) {
        return { action: "buy", reasoning: "It's cheap and I can afford it" };
      }
      return { action: "pass", reasoning: "Too expensive or risky" };
      
    case "Medium rare":
      // Moderate strategy: consider rent ratio and affordability
      if (affordability > 2 && rentRatio > 0.08) {
        return { action: "buy", reasoning: "Good rent-to-price ratio" };
      }
      if (affordability > 4 && property.price < 200) {
        return { action: "buy", reasoning: "Safe investment" };
      }
      return { action: "pass", reasoning: "Not a good value" };
      
    case "Highly proficient":
      // Advanced strategy: complex decision making
      const expectedReturn = rentRatio * 0.7; // Accounting for vacancy
      const riskFactor = property.price > 250 ? 1.5 : 1.0;
      
      if (affordability > 2.5 && expectedReturn > 0.06 / riskFactor) {
        return { action: "buy", reasoning: "Strong ROI potential" };
      }
      if (bot.properties.length < 2 && affordability > 3) {
        return { action: "buy", reasoning: "Portfolio diversification" };
      }
      if (property.type === "railroad" && affordability > 2) {
        return { action: "buy", reasoning: "Strategic railroad acquisition" };
      }
      return { action: "pass", reasoning: "Suboptimal investment opportunity" };
      
    default:
      return { action: "pass", reasoning: "Unknown strategy" };
  }
};

// Mock API functions that will be replaced with real backend calls
export const mockAPI = {
  startGame: () => {
    return Promise.resolve(mockGameData.initialGameState);
  },
  
  rollDice: (playerId) => {
    const dice1 = Math.floor(Math.random() * 6) + 1;
    const dice2 = Math.floor(Math.random() * 6) + 1;
    return Promise.resolve({ dice1, dice2, total: dice1 + dice2 });
  },
  
  buyProperty: (playerId, propertyId) => {
    return Promise.resolve({ success: true });
  },
  
  payRent: (payerId, receiverId, amount) => {
    return Promise.resolve({ success: true });
  },
  
  getBotDecision: (botId, propertyId) => {
    return Promise.resolve({ action: "buy" }); // Simplified for mock
  }
};