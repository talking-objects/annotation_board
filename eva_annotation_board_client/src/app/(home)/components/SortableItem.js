"use client"

import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import Item from "./Item";

function SortableItem({data, setItems, containerId}) {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id: data.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div ref={setNodeRef} style={style} >
      <Item data={data} containerId={containerId} setItems={setItems} attributes={attributes} listeners={listeners} />
      
    </div>
  );
}

export default SortableItem;
