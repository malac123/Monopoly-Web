import GameBoard from "./components/GameBoard";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<GameBoard />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
