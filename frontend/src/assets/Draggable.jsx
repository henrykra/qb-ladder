import React from 'react';
import {useDraggable} from '@dnd-kit/core';
import {CSS} from '@dnd-kit/utilities';

export default function Draggable(props) {
  const {attributes, listeners, setNodeRef, transform} = useDraggable({
    id: props.id,
    disabled: props.locked,
  });
  const style = {
    // Outputs `translate3d(x, y, 0)`
    transform: CSS.Translate.toString(transform),
    cursor: props?.locked ? 'default' : 'move',
  };

  return (
    <div ref={setNodeRef} style={style} {...listeners} {...attributes} className="cursor-move inline-block">
      {props.children}
    </div>
  );
}
