import { FiHome, FiList } from "react-icons/fi";

import { Sidebar, SidebarItem } from "./components";

import {Itens} from "./pages";

function App() {
  return (
    <div className="App">
      <div className="w-full bg-dark-5 flex flex-row">
        <Sidebar>
          <SidebarItem icon={<FiHome></FiHome>} title="Provas"></SidebarItem>
          <SidebarItem icon={<FiList></FiList>} title="Questões"></SidebarItem>
        </Sidebar>
        <div className="w-full">
          <Itens></Itens>
        </div>
      </div>
    </div>
  );
}

export default App;
