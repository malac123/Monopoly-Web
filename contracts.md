# Monopoly Game - Backend Integration Contracts

## API Contracts

### Game Management
- `POST /api/games` - Create new game session
- `GET /api/games/{gameId}` - Get game state
- `PUT /api/games/{gameId}/start` - Start game
- `DELETE /api/games/{gameId}` - Delete game

### Player Actions  
- `POST /api/games/{gameId}/roll-dice` - Roll dice for current player
- `POST /api/games/{gameId}/buy-property` - Buy current property
- `POST /api/games/{gameId}/decline-property` - Decline property purchase
- `GET /api/games/{gameId}/current-player` - Get current player info

### Bot AI
- `POST /api/games/{gameId}/bot-decision` - Get bot decision for property
- `POST /api/games/{gameId}/bot-turn` - Execute complete bot turn

### Game Data
- `GET /api/properties` - Get all property definitions
- `GET /api/games/{gameId}/properties` - Get properties with ownership
- `GET /api/games/{gameId}/players` - Get all players with stats

## Mock Data to Replace

### From `mock.js`:
1. **Properties Array** (20 properties) → MongoDB `properties` collection
2. **Game State** → MongoDB `games` collection:
   - Players array with money, position, properties
   - Current player index
   - Game phase and winner
3. **Bot Decision Engine** → Backend AI logic
4. **Mock API functions** → Real FastAPI endpoints

### Data Models Needed:
```python
# Property Model
class Property(BaseModel):
    id: int
    name: str
    type: str  # property, railroad, utility, special
    color: str
    price: Optional[int]
    rent: Optional[int]
    owner: Optional[int]
    description: Optional[str]

# Player Model  
class Player(BaseModel):
    id: int
    name: str
    money: int
    position: int
    properties: List[int]
    isBot: bool
    difficulty: Optional[str]

# Game State Model
class GameState(BaseModel):
    id: str
    players: List[Player]
    currentPlayerIndex: int
    gamePhase: str  # playing, ended
    winner: Optional[int]
    createdAt: datetime
    lastMove: Optional[dict]
```

## Backend Implementation Plan

### 1. Database Schema
- `games` collection - Store game sessions
- `properties` collection - Store property definitions (seeded data)
- `game_logs` collection - Store move history for debugging

### 2. Core Game Logic
- **Dice rolling** with random generation
- **Player movement** with GO bonus logic  
- **Property ownership** tracking and transfers
- **Rent calculation** and payment processing
- **Bot AI decision engine** with difficulty-based strategies

### 3. Turn Management
- **Turn progression** validation
- **Bot turn automation** with timed decisions
- **Game state persistence** after each move
- **Win condition checking**

### 4. Bot AI Engine
Migrate from frontend mock to backend:
- **Mentally slow**: Simple price-based decisions
- **Medium rare**: Rent ratio and affordability analysis  
- **Highly proficient**: Complex ROI and strategy calculations

## Frontend Integration Changes

### Remove Mock Dependencies:
1. Replace `mockGameData` imports with API calls
2. Remove `botDecisionEngine` frontend logic  
3. Replace `mockAPI` with axios calls to backend

### API Integration Points:
1. **GameBoard.js**: 
   - `useEffect` to load game on mount
   - Replace dice roll logic with API call
   - Replace property buy/decline with API calls

2. **PlayerPanel.js**:
   - Real-time player data from API
   - Property ownership from backend

3. **PropertyCard.js**:  
   - Backend validation for purchase ability
   - Real money deduction through API

4. **DiceRoller.js**:
   - API call for dice roll with backend validation

### State Management:
- Replace local state with backend-synced state
- Add loading states for API calls
- Add error handling for network issues
- Real-time updates for bot moves

## Testing Strategy

### Backend Testing:
1. **Unit Tests**: Game logic, bot AI, property transactions
2. **Integration Tests**: Full game flow, API endpoints
3. **Load Tests**: Multiple concurrent games

### Frontend Integration Testing:
1. **Game Flow**: Complete game from start to finish  
2. **Bot Behavior**: All difficulty levels working
3. **Error Handling**: Network failures, invalid moves
4. **Performance**: Smooth animations with API calls

## Success Criteria

✅ **Backend Ready**: All API endpoints working
✅ **Frontend Integrated**: Mock data completely replaced  
✅ **Game Playable**: Full game flow with persistence
✅ **Bots Working**: AI decisions made by backend
✅ **Error Handling**: Graceful failure management
✅ **Performance**: Sub-500ms API response times