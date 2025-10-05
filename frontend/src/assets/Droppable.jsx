import React from 'react';
import {useDroppable} from '@dnd-kit/core';

export default function Droppable(props) {
  const {isOver, setNodeRef} = useDroppable({
    id: props.id,
  });
  const style = {
    borderColor: isOver || props?.full ? 'cyan' : 'white',
    opacity: isOver && props?.full ? '.5' : '1',
    borderStyle: props?.locked ? 'solid' : 'dashed'
  };

  return (
    <div ref={setNodeRef} style={style} className='bg-slate-600/65 lg:size-32 md:size-21 border-3 rounded-xl
                                                   md:text-base sm:size-18 sm:text-xs
                                                   border-gray-50 inset-shadow-sm/20 shadow-md/20 
                                                   flex items-center justify-center transition-all ease-in-out duration-100'>
      {props.children}
    </div>
  );
}
  