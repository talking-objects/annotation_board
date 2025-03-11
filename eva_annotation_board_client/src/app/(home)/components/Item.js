import { CLayerItemName, DLayerItemName, ELayerItemName, Layers, LayersColor, LayersName } from "@/app/utils/constants/layers";
import { useState } from "react";
import { useForm } from "react-hook-form";

const Item = ({ data, attributes, listeners, setItems, containerId }) => {
  const [isEdit, setIstEdit] = useState(false);
  const { getValues, register, setValue } = useForm();
  const onDelete = () => {
    console.log(containerId);
    // Delete Item
    const items = JSON.parse(localStorage.getItem("toaItemList"));
    const currentIndex = items.children.findIndex((val) => val.id === containerId);
    const currentContainer = items.children[currentIndex];
    const currentItemIndex = currentContainer.list.findIndex((val) => val.id === data.id);
    currentContainer.list.splice(currentItemIndex, 1);
    console.log(currentContainer);
    console.log(items.children[currentIndex]);
    items.children[currentIndex] = currentContainer;
    setItems((prev) => {
      return {
        ...prev,
        children: [...items.children],
      };
    });
    localStorage.setItem("toaItemList", JSON.stringify(items));
    console.log(items);
  };

  const onEdit = () => {
    if (!isEdit) {
      // Edit
      setIstEdit(true);
    } else {
      // Save
      const items = JSON.parse(localStorage.getItem("toaItemList"));
      const currentIndex = items.children.findIndex((val) => val.id === containerId);
      const currentContainer = items.children[currentIndex];
      const currentItemIndex = currentContainer.list.findIndex((val) => val.id === data.id);

      const newInput = getValues("editInput");

      const getLayer = currentContainer.list[currentItemIndex].layer;
      let getInput = {};
      if (getLayer === Layers[0]) {
        getInput.value = getValues("a_layer_input");
      } else if (getLayer === Layers[1]) {
        getInput.value = getValues("b_layer_input");
      } else if (getLayer === Layers[2]) {
        getInput.value = {
          url: getValues("c_layer_input1"),
          text: getValues("c_layer_input2")
        };
      } else if (getLayer === Layers[3]) {
        const values = getValues("d_layer_input");
        getInput.value = values
      } else if (getLayer === Layers[4]) {
        getInput.value = {
          text: getValues("e_layer_input1"),
          url: getValues("e_layer_input2"),
        };
      } else if (getLayer === Layers[5]) {
        getInput.value = {
          text: getValues("f_layer_input1"),
          startDate: new Date(getValues("f_layer_input2")),
          endDate: new Date(getValues("f_layer_input3")),
        };
      } else if (getLayer === Layers[6]) {
        getInput.value = {
          url: getValues("g_layer_input1"),
          placeName: getValues("g_layer_input2"),
          text: getValues("g_layer_input3"),
          latitude: getValues("g_layer_input4"),
          longitude: getValues("g_layer_input5"),
        };
      }
      currentContainer.list[currentItemIndex].input = getInput;
      items.children[currentIndex] = currentContainer;
      setItems((prev) => {
        return {
          ...prev,
          children: [...items.children],
        };
      });
      localStorage.setItem("toaItemList", JSON.stringify(items));
      setIstEdit(false);
    }
  };
  if (!Boolean(data)) {
    return (
      <div className="w-full bg-white flex justify-center items-center rounded-md py-8 drop-shadow-lg">
        <div className="flex gap-3">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M10.05 4.575a1.575 1.575 0 1 0-3.15 0v3m3.15-3v-1.5a1.575 1.575 0 0 1 3.15 0v1.5m-3.15 0 .075 5.925m3.075.75V4.575m0 0a1.575 1.575 0 0 1 3.15 0V15M6.9 7.575a1.575 1.575 0 1 0-3.15 0v8.175a6.75 6.75 0 0 0 6.75 6.75h2.018a5.25 5.25 0 0 0 3.712-1.538l1.732-1.732a5.25 5.25 0 0 0 1.538-3.712l.003-2.024a.668.668 0 0 1 .198-.471 1.575 1.575 0 1 0-2.228-2.228 3.818 3.818 0 0 0-1.12 2.687M6.9 7.575V12m6.27 4.318A4.49 4.49 0 0 1 16.35 15m.002 0h-.002"
            />
          </svg>
          <div className="text-xl font-medium">Go ahead, drag me</div>
        </div>
      </div>
    );
  }
  return (
    <div className="w-full h-fit min-h-9 bg-white drop-shadow-md overflow-hidden rounded-md flex flex-col">
      <button {...attributes} {...listeners} style={{ backgroundColor: `${LayersColor[data?.layer]}` }} className="flex py-2 px-2 justify-between items-center hover:opacity-80">
        <div className="text-white font-semibold text-sm">{LayersName[data?.layer]}</div>
      </button>
      {!isEdit && (
        <div className="px-2 py-2 text-wrap break-words text-sm">
          {data?.layer === Layers[0] && <div>{data?.input.value}</div>}
          {data?.layer === Layers[1] && <div>{data?.input.value}</div>}
          {data?.layer === Layers[2] && (
            <div>
              {Object.keys(data?.input.value).map((v) => {
                return (
                  <div key={v}>
                    <span className="font-medium">{v}</span> : {String(data?.input.value[v])}
                  </div>
                );
              })}
            </div>
          )}
          {data?.layer === Layers[3] && (
            <div>
              <span className="font-medium">{DLayerItemName[data?.input.value]}</span>
            </div>
          )}
          {data?.layer === Layers[4] && (
            <div>
              {Object.keys(data?.input.value).map((v) => {
                return (
                  <div key={v}>
                    <span className="font-medium">{v}</span> : {String(data?.input.value[v])}
                  </div>
                );
              })}
            </div>
          )}
          {data?.layer === Layers[5] && (
            <div>
              {
                Object.keys(data?.input.value).map((v) => {
                  return (
                    <div key={v}>
                      <span className="font-medium">{v}</span> : {String(data?.input.value[v])}
                    </div>
                  );
                })
              }
            </div>
          )}
          {data?.layer === Layers[6] && (
            <div>
              {
                Object.keys(data?.input.value).map((v) => {
                  return (
                    <div key={v}>
                      <span className="font-medium">{v}</span> : {String(data?.input.value[v])}
                    </div>
                  );
                })  
              }
            </div>
          )}
        </div>
      )}
      {isEdit && (
        <div className="w-full px-2 py-2">
          <div className="w-full mt-2">
            {data?.layer === Layers[0] && <input required defaultValue={data.input.value} type="text" {...register("a_layer_input")} className="w-full border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="Write tags...#example #art" />}
            {data?.layer === Layers[1] && <textarea required defaultValue={data.input.value} {...register("b_layer_input")} className="w-full border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="Write text..." />}
            {data?.layer === Layers[2] && (
              <div className="w-full flex flex-col gap-2">
                <input type="url" defaultValue={data.input.value.url} {...register("c_layer_input1")} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="URL" />
                <input required type="text" defaultValue={data.input.value.text} {...register("c_layer_input2")} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="Text" />
              </div>
            )}
            {data?.layer === Layers[3] && (
               <div className="w-full flex flex-col gap-2">
               <div className="flex gap-2">
                 <input type="radio" name="d_layer_input" value="a" defaultChecked={data.input.value === "a"} {...register("d_layer_input", { required: true })} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" />
                 <label htmlFor="d_layer_input">{DLayerItemName["a"]}</label>
               </div>
               <div className="flex gap-2">
                 <input type="radio" name="d_layer_input" value="b" defaultChecked={data.input.value === "b"} {...register("d_layer_input", { required: true })} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" />
                 <label htmlFor="d_layer_input">{DLayerItemName["b"]}</label>
               </div>
               <div className="flex gap-2">
                 <input type="radio" name="d_layer_input" value="c" defaultChecked={data.input.value === "c"} {...register("d_layer_input", { required: true })} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" />
                 <label htmlFor="d_layer_input">{DLayerItemName["c"]}</label>
               </div>
               <div className="flex gap-2">
                 <input type="radio" name="d_layer_input" value="d" defaultChecked={data.input.value === "d"} {...register("d_layer_input", { required: true })} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" />
                 <label htmlFor="d_layer_input">{DLayerItemName["d"]}</label>
               </div>
               <div className="flex gap-2">
                 <input type="radio" name="d_layer_input" value="e" defaultChecked={data.input.value === "e"} {...register("d_layer_input", { required: true })} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" />
                 <label htmlFor="d_layer_input">{DLayerItemName["e"]}</label>
               </div>
             </div>
            )}
            {data?.layer === Layers[4] && (
              <div className="w-full flex flex-col gap-2">
                <input required type="text" defaultValue={data.input.value.text} {...register("e_layer_input1")} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="Text" />
                <input type="url" defaultValue={data.input.value.url} {...register("e_layer_input2")} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="URL" />
              </div>
            )}
            {data?.layer === Layers[5] && (
                <div className="w-full flex flex-col gap-2">
                <textarea {...register("f_layer_input1")} required className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="Text" />
                <div className="flex flex-col gap-1">
                  <label htmlFor="f_layer_input2" className="text-sm font-medium">Start Date</label>
                  <input required type="date" {...register("f_layer_input2")} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="Start Date" />
                </div>
                <div className="flex flex-col gap-1">
                  <label htmlFor="f_layer_input3" className="text-sm font-medium">End Date</label>
                  <input required type="date" {...register("f_layer_input3")} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="End Date" />
                </div>
              </div>
            )}
            {data?.layer === Layers[6] && (
                <div className="w-full flex flex-col gap-2">
                <input type="text" {...register("g_layer_input1")} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="URL" />
                <input required type="text" {...register("g_layer_input2")} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="Place Name" />
                <textarea {...register("g_layer_input3")} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="Text" />
                <div className="flex gap-2">
                  <input 
                    required
                    type="number" 
                    step="0.000001"
                    {...register("g_layer_input4")} 
                    className="w-1/2 border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" 
                    placeholder="Latitude" 
                  />
                  <input 
                    required
                    type="number"
                    step="0.000001" 
                    {...register("g_layer_input5")} 
                    className="w-1/2 border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" 
                    placeholder="Longitude" 
                  />
                </div>
              </div>
            )}
          </div>
        </div>
      )}
      <div className="w-full flex justify-end text-neutral-800 mt-4">
        <div onClick={() => onEdit()} className="px-2 py-2 cursor-pointer text-neutral-600 text-sm font-semibold hover:text-orange-400">
          {!isEdit && "Edit"}
          {isEdit && "Save"}
        </div>
        <div onClick={() => onDelete()} className="px-2 py-2 cursor-pointer text-neutral-600 text-sm font-semibold hover:text-orange-400">
          Delete
        </div>
      </div>
    </div>
  );
};

export default Item;
