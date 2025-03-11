"use client";
import { useDroppable } from "@dnd-kit/core";
import SortableItem from "./SortableItem";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { DLayerItemName, Layers, LayersName } from "@/app/utils/constants/layers";

const { SortableContext } = require("@dnd-kit/sortable");
import { v4 as uuidv4 } from 'uuid';

const Container = ({ id, items, time, setItems, onShowVideo }) => {
  const [isEdit, setIsEdit] = useState(false);
  const [currentLayer, setCurrentLayer] = useState("");
  const {
    register,
    handleSubmit,
    watch,
    setValue,
    getValues,
    formState: { errors },
  } = useForm();
  const { setNodeRef } = useDroppable({
    id: id,
  });

  const watchLayer = watch("layerselect");
  useEffect(() => {
    
    const getLayerValue = getValues("layerselect");
    setCurrentLayer(getLayerValue);
  }, [watchLayer, isEdit]);
  const onSubmit = () => {
    addLayer(false);
  };
  const addLayer = (edit) => {
    if (edit) {
      setIsEdit(edit);
    } else {
      // 👨‍💻
      const getLayer = getValues("layerselect");
      let getInput = {};
      if (getLayer === Layers[0]) {
        // Tag Layer
        getInput.value = getValues("a_layer_input");
      } else if (getLayer === Layers[1]) {
        // Narration Layer
        getInput.value = getValues("b_layer_input");
      } else if (getLayer === Layers[2]) {
        // Data Layer
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
  
      const items = JSON.parse(localStorage.getItem("toaItemList"));
  
      const currentIndex = items.children.findIndex((val) => val.id === id);
    
      items.children[currentIndex].list.push({
        id: `${uuidv4()}`,
        layer: getLayer,
        input: getInput,
      });
      setItems(items);
      localStorage.setItem("toaItemList", JSON.stringify(items));
      setIsEdit(edit);
      setValue("layerselect", Layers[0]);
      setValue("a_layer_input", "");
    }
  };

  function convertSecondsToTime(seconds) {
    // Check if the input is a number
    if (isNaN(seconds)) {
      return "Input is not a number";
    }

    // Calculate hours, minutes, and seconds
    let hours = Math.floor(seconds / 3600);
    let remainingSecondsAfterHours = seconds % 3600;
    let minutes = Math.floor(remainingSecondsAfterHours / 60);
    let remainingSeconds = remainingSecondsAfterHours % 60;

    // Format with leading zeros
    let hoursString = hours.toString().padStart(2, "0");
    let minutesString = minutes.toString().padStart(2, "0");
    let secondsString = remainingSeconds.toString().padStart(2, "0");

    // Return the result as a string
    return `${hoursString}:${minutesString}:${secondsString}`;
  }

  return (
    <SortableContext id={id} items={items}>
      <div id={`a${id}`} ref={setNodeRef} className="driver-a w-[400px] max-h-[calc(100vh-20px-16px-55px)] overflow-y-scroll flex flex-col gap-3 min-h-10 bg-neutral-100 rounded-md p-2 relative">
        <div className="w-full text-sm text-neutral-850 font-medium flex justify-between items-center px-2 py-2 sticky top-0 left-0 z-50 bg-white drop-shadow-lg">
          <div className="">
            {convertSecondsToTime(time[0])} to {convertSecondsToTime(time[1])}
          </div>
          <div onClick={() => onShowVideo({seek: parseInt(time[0])})} className="driver-c cursor-pointer hover:text-orange-500">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.0} stroke="currentColor" className="size-6">
              <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 3.75H6A2.25 2.25 0 0 0 3.75 6v1.5M16.5 3.75H18A2.25 2.25 0 0 1 20.25 6v1.5m0 9V18A2.25 2.25 0 0 1 18 20.25h-1.5m-9 0H6A2.25 2.25 0 0 1 3.75 18v-1.5M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
            </svg>
          </div>
        </div>
        {items.map((val) => {
          return <SortableItem key={val.id} containerId={id} data={val} setItems={setItems} />;
        })}
        {!isEdit && (
          <div onClick={() => addLayer(true)} className="driver-b w-full border-2 border-black border-dashed py-2 text-black flex justify-center opacity-35 rounded-md cursor-pointer transition-all hover:opacity-100 hover:bg-black hover:text-white">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-8">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
          </div>
        )}
        {isEdit && (
          <form onSubmit={handleSubmit(onSubmit)} className="driver-c w-full bg-white border-2 border-black py-2 px-2 text-black flex flex-col gap-2 justify-center rounded-md cursor-pointer transition-all">
            <label htmlFor="layer" className="font-medium text-sm text-neutral-950">
              Select a Layer
            </label>
            <select id="layer" defaultValue={Layers[0]} {...register("layerselect")} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400">
              {Layers.map((val) => {
                return (
                  <option key={val} value={val}>
                    {LayersName[val]}
                  </option>
                );
              })}
            </select>
            {currentLayer === Layers[0] && <input type="text" {...register("a_layer_input")} required className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="Write tags, divide using comma" />}
            {currentLayer === Layers[1] && <textarea {...register("b_layer_input")} required className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="Write text..." />}
            {currentLayer === Layers[2] && (
              <div className="w-full flex flex-col gap-2">
                <input type="url" {...register("c_layer_input1")} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="URL" />
                <input type="text" {...register("c_layer_input2")} required className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="Text" />
              </div>
            )}
            {currentLayer === Layers[3] && (
              <div className="w-full flex flex-col gap-2">
                <div className="flex gap-2">
                  <input type="radio" name="d_layer_input" value="a" {...register("d_layer_input", { required: true })} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" />
                  <label htmlFor="d_layer_input">{DLayerItemName["a"]}</label>
                </div>
                <div className="flex gap-2">
                  <input type="radio" name="d_layer_input" value="b" {...register("d_layer_input", { required: true })} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" />
                  <label htmlFor="d_layer_input">{DLayerItemName["b"]}</label>
                </div>
                <div className="flex gap-2">
                  <input type="radio" name="d_layer_input" value="c" {...register("d_layer_input", { required: true })} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" />
                  <label htmlFor="d_layer_input">{DLayerItemName["c"]}</label>
                </div>
                <div className="flex gap-2">
                  <input type="radio" name="d_layer_input" value="d" {...register("d_layer_input", { required: true })} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" />
                  <label htmlFor="d_layer_input">{DLayerItemName["d"]}</label>
                </div>
                <div className="flex gap-2">
                  <input type="radio" name="d_layer_input" value="e" {...register("d_layer_input", { required: true })} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" />
                  <label htmlFor="d_layer_input">{DLayerItemName["e"]}</label>
                </div>
              </div>
            )}
            {currentLayer === Layers[4] && (
              <div className="w-full flex flex-col gap-2">
                <input type="text" {...register("e_layer_input1")} required className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="Text" />
                <input type="url" {...register("e_layer_input2")} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="URL" />
              </div>
            )}
            {currentLayer === Layers[5] && (
              <div className="w-full flex flex-col gap-2">
                <textarea {...register("f_layer_input1")} required className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="Text" />
                <div className="flex flex-col gap-1">
                  <label htmlFor="f_layer_input2" className="text-sm font-medium">Start Date</label>
                  <input type="date" {...register("f_layer_input2")} required className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="Start Date" />
                </div>
                <div className="flex flex-col gap-1">
                  <label htmlFor="f_layer_input3" className="text-sm font-medium">End Date</label>
                  <input type="date" {...register("f_layer_input3")} required className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="End Date" />
                </div>
              </div>
            )}
            {
              currentLayer === Layers[6] && (
                <div className="w-full flex flex-col gap-2">
                  <input type="text" {...register("g_layer_input1")} className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="URL" />
                  <input type="text" {...register("g_layer_input2")} required className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400" placeholder="Place Name" />
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
              )
            }
            <input type="submit" value="Create Layer" className="w-full text-white text-sm font-semibold bg-neutral-900 rounded-md py-2 cursor-pointer" />
          </form>
        )}
      </div>
    </SortableContext>
  );
};

export default Container;
