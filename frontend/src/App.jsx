import React, { useState, useEffect } from 'react'
import './App.css'

// drag-and-drop functionality
import { DndContext, DragOverlay } from '@dnd-kit/core'
import Draggable from './assets/Draggable';
import StreamText from './assets/StreamText';

// custom assets
import PlayerIcon from './assets/PlayerIcon';
import Ladder from './assets/Ladder';
import Container from './assets/Container';

const NUM_RANKS = 4;


function App() {
  const [activeId, setActiveId] = useState(null);
  const [dragOrigin, setDragOrigin] = useState(null);
  const [ranks, setRanks] = useState(Array(NUM_RANKS).fill(null));
  const [locked, setLocked] = useState(false);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(Array(NUM_RANKS).fill({
    primaryColor: '#FFFFFF',
    secondaryColor: '000000',
    lastName: 'test',
    src: 'public/qb-faces/default.png'
  }))

  const ids = [33106, 34869, 36264, 39918]
  

  // make player icon data a state variable, wrapped in useEffect that runs on startup. 
  // then simple set of draggables according to the state variable
  useEffect(() => {
    async function fetchData(id) {
      const responseColor = await fetch(`/api/color/${id}`);
      const jsonColor = await responseColor.json();

      const responsePlayer = await fetch(`/api/player/${id}`);
      const jsonPlayer = await responsePlayer.json();

      return ({
        src: 'qb-faces/' + String(id) + '.png',
        primaryColor: jsonColor.primary_color,
        secondaryColor: jsonColor.secondary_color,
        lastName: jsonPlayer.last_name,
        name: jsonPlayer.name,
        id: id,
      });
    }

    async function loadData() {
      const promises = ids.map(id => fetchData(id));
      const results = await Promise.all(promises);
      setData(results)
    }
   loadData();
  }, [])

  // Create player icon draggables
  const draggables = data.map((data, index) => (
    <Draggable id={String(index)} key={index} locked={locked} pid={data.id}>
      <PlayerIcon src={data.src} lastName={data.lastName} primaryColor={data.primaryColor} secondaryColor={data.secondaryColor}/>
    </Draggable>
  ))

  return (
    <DndContext onDragEnd={handleDragEnd} onDragStart={handleDragStart}>
      
      <div
        className='relative flex flex-row items-center h-full'
      >

        {/* Ladder div containing ranks */}
        <Ladder ranks={ranks} draggables={draggables} locked={locked} 
                loading={loading} handleReset={handleReset} />

        {/* vertical flex containing players and chat window*/}
        <div
          className='flex flex-col items-center self-start justify-end min-h-full
                     transition-all ease-in-out duration-100'
        >
          {/* Hero image */}
          <img
            src='hero.png'
            className='lg:w-110 lg:h-35 md:w-70 md:h-30 sm:w-45 sm:h-20 transition-all ease-in-out duration-100'
          />

          {/* Chat window */}
          <div
            className='lg:w-200 md:w-140 sm:w-85 lg:h-100 md:h-65 sm:h-53 flex-shrink'
          >
            <StreamText enabled={!(ranks.includes(null) | ranks.includes(undefined))}
              locked={locked} setLocked={setLocked} loading={loading} setLoading={setLoading}
              ranks={ranks} draggables={draggables}
            />
          </div>

          {/* Player container box */}
          <Container draggables={draggables} ranks={ranks} activeId={activeId} />
        </div>
      </div> 

      <DragOverlay>
        {activeId ? (
          draggables[activeId]
        ): null}
      </DragOverlay>

    </DndContext>
  );

  function handleDragEnd({ active, over }) {
    
    setRanks(prev => {
      const newRanks = [ ...prev ]
      // if the destination has an item, swap it to the drag origin
      if (dragOrigin !== null && over?.id !== null) {
        newRanks[dragOrigin] = newRanks[over?.id]
      }
      // if the destination is a rank, upate it
      newRanks[over?.id] = active.id;

      return newRanks
    })
    setActiveId(null);

    // console.log(active.rect.current.initial);
    // console.log(active.rect.current.translated);
    // translate the occupying icon to the initial location of the active icon
  }

  function handleDragStart({ active, event }) {
    setActiveId(active.id);
    const newRanks = [...ranks]

    for (let i = 0; i < newRanks.length; i++) {
      if (newRanks[i] === active.id){
        setDragOrigin(i); // set the source of the drag
        newRanks[i] = null; // remove the active object from its rank
        setRanks(newRanks); 
        return;
      }
    }
    setDragOrigin(null);
  }

  function handleReset() {
    setLocked(false);
  }

}

export default App
