"use client";

import {
  DndContext,
  DragOverlay,
  closestCorners,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
} from "@dnd-kit/core";
import { useEffect, useId, useRef, useState } from "react";
import Container from "./Container";
import { arrayMove, sortableKeyboardCoordinates } from "@dnd-kit/sortable";
import Item from "./Item";
import { useForm } from "react-hook-form";
import ReactPlayer from "react-player";
import Nav from "./Nav";
import { BASE_URL } from "@/app/utils/constants/pandora";
import { v4 as uuidv4 } from 'uuid';
import { fetchPandora } from "@/app/utils/hooks/fetchPandora";
import { useUser } from "@/app/utils/hooks/useUser";
import { logout, uploadVideo } from "@/app/api";
import { CategoryLayerItemData } from "@/app/utils/constants/layers";


const TWrapper = ({pandora}) => {
  // const [items, setItems] = useRecoilState(itemsAtom);
  // const [pandora, setPandora] = useState([])
  const [done, setDone] = useState(false);
  const [items, setItems] = useState([]);
  const [activeId, setActiveId] = useState();
  // const items = createFakeData({ containerCount: 4 });
  const contextId = useId();
  const [ready, setReady] = useState(true);
  const [aktiv, setAktiv] = useState(true);
  const [showVideo, setShowVideo] = useState(false);
  const [showVideoURL, setShowVideoURL] = useState("");
  const { register, watch, setValue, getValues, handleSubmit } = useForm({});
  const videoRef = useRef();
  const [currentVideoUrl, setCurrentVideoUrl] = useState("");
  const [checkURL, setCheckURL] = useState(false);
  const timeLineVideoRef = useRef();
  const seekTime = useRef(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const scrollRef = useRef();

  const { user } = useUser();

  useEffect(() => {
    const getLocalItems = JSON.parse(localStorage.getItem("toaItemList"));
    if (!Boolean(getLocalItems)) {
      setReady(false);
    } else {
      setItems(getLocalItems);
    }
  }, []);

  const defaultAnnouncements = {
    onDragStart(id) {
      // console.log(`Picked up draggable item ${id}.`);
    },
    onDragOver(id, overId) {
      if (overId) {
        // console.log(
        //   `Draggable item ${id} was moved over droppable area ${overId}.`
        // );
        return;
      }

      // console.log(`Draggable item ${id} is no longer over a droppable area.`);
    },
    onDragEnd(id, overId) {
      if (overId) {
        // console.log(
        //   `Draggable item ${id} was dropped over droppable area ${overId}`
        // );
        return;
      }

      // console.log(`Draggable item ${id} was dropped.`);
    },
    onDragCancel(id) {
      // console.log(`Dragging was cancelled. Draggable item ${id} was dropped.`);
    },
  };

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  function findContainer(id) {
    // if (id in items) {
    //   return id;
    // }

    // return Object.keys(items).find((key) => items[key].includes(id));
    const findIndex = items.children.findIndex((v) => v.id === id);
    // console.log(findIndex)
    return findIndex;
  }

  function handleDragStart(event) {
    const { active } = event;
    const { id } = active;

    setActiveId(id);
  }

  function handleDragOver(event) {

    const { active, over, draggingRect } = event;
    // console.log(active, over);
    // const {
    //   data: {
    //     current: {
    //       sortable: { containerId },
    //     },
    //   },
    // } = active;
    // const { id: overId, data: {current: {sortable: {containerId: overContainerId}}} } = over;
    // console.log(active, over);

    // const activeContainer = findContainer(containerId);
    let activeContainer = "";
    activeContainer = findContainer(active.data.current?.sortable?.containerId);
    let overContainer = "";
    overContainer = findContainer(over.data.current?.sortable?.containerId);

    if (
      !String(activeContainer) ||
      !String(overContainer) ||
      String(activeContainer) === String(overContainer)
    ) {
      // console.log(activeContainer, overContainer);
      return;
    }
    if (
      !Boolean(over.data.current?.sortable?.containerId) &&
      over.id === active.data.current?.sortable?.containerId
    ) {
    
      return;
    }

    const result = items;

    const activeItems = result.children[activeContainer];

    let overContainer2;
    if (over.data.current) {
      overContainer2 = overContainer;
    } else {
      overContainer2 = findContainer(over.id);
    }
    const overItems = result.children[overContainer2];

    const activeIndex = activeItems.list.findIndex(
      (v) => String(v.id) === String(active.id)
    );
    const overIndex = overItems.list.findIndex((v) => v.id === over.id);
    // console.log(activeIndex, overIndex);
    // console.log(overContainer2);
    let newIndex;

    if (active.id !== over.id) {
      newIndex = overItems.list.length + 1;
    }

    result.children[overContainer2].list = [
      ...items.children[overContainer2].list.slice(0, newIndex),
      items.children[activeContainer].list[activeIndex],
      ...items.children[overContainer2].list.slice(
        newIndex,
        items.children[overContainer2].list.length
      ),
    ];
    result.children[activeContainer].list = [
      ...items.children[activeContainer].list.filter(
        (item) => item.id !== active.id
      ),
    ];

    localStorage.setItem("toaItemList", JSON.stringify(result));
    setItems((prev) => {
      return {
        ...prev,
        children: [...result.children],
      };
    });
  }

  function handleDragEnd(event) {
    const { active, over } = event;
    let activeContainer = "";
    activeContainer = findContainer(active.data.current?.sortable?.containerId);
    let overContainer = "";
    overContainer = findContainer(over.data.current?.sortable?.containerId);

    if (
      !String(activeContainer) ||
      !String(overContainer) ||
      String(activeContainer) !== String(overContainer)
    ) {
      return;
    }
    const activeIndex = items.children[activeContainer].list.findIndex(
      (v) => String(v.id) === String(active.id)
    );
    const overIndex = items.children[overContainer].list.findIndex(
      (v) => v.id === over.id
    );
 
    if (String(activeIndex) !== String(overIndex)) {
      // console.log(items)
   
      const result = items;
    
      result.children[overContainer].list = arrayMove(
        items.children[overContainer].list,
        activeIndex,
        overIndex
      );
      localStorage.setItem("toaItemList", JSON.stringify(result));
      setItems((prev) => {
        return {
          ...prev,
          children: [...result.children],
        };
      });
    }

    // setActiveId(null);
  }

  const onUploadVideo = () => {
    const videoURL = getValues("videoURL");

    if (videoRef.current) {
      if (ReactPlayer.canPlay(`${BASE_URL}/${videoURL}/480p1.mp4`)) {
        setCurrentVideoUrl(`${BASE_URL}/${videoURL}/480p1.mp4`);
      } else {
       
        setCheckURL(true);
      }
    }
  };

  const getContainers = ({
    seconds,
    timeGap,
    description = "null",
    contributors = "null",
    place = "null",
    languages = "null",
    gerne = "null",
    source = "null",
    author = "null",
    country = "null",
    title = "null",
  }) => {
  
    // 100 / 30
    const getSeconds = seconds;
    const containerCount = Math.ceil(getSeconds / timeGap);
   
    let time = [];
    const itemsData = {
      title: title,
      author: author,
      contributors: contributors,
      place: place,
      languages: languages,
      gerne: gerne,
      source: source,
      description: description,
      country: country,
      children: [],
    };
    for (let i = 0; i < containerCount; i++) {
      if (i === 0) {
        time = [0, (i + 1) * timeGap];
      } else {
        if ((i + 1) * timeGap > getSeconds) {
          time = [i * timeGap, Math.floor(getSeconds)];
        } else {
          time = [i * timeGap, (i + 1) * timeGap];
        }
      }
      const containerItemsList = {};
      containerItemsList.id = `${uuidv4()}`;
      containerItemsList.list = [];
      containerItemsList.time = time;
      itemsData.children.push(containerItemsList);
    }
    // console.log(itemsData);
    localStorage.setItem("toaItemList", JSON.stringify(itemsData));
    setItems(itemsData);
  };

  const onAboutVideo = () => {
    if (videoRef.current) {
      const duration = videoRef.current.getDuration();
      const title = getValues("title");
      const timeGap = parseInt(getValues("timeGapSection"));
      const author = getValues("author");
      const description = getValues("description");
      const contributors = getValues("contributors");
      const country = getValues("country");
      const place = getValues("place");
      const source = getValues("source");
      const languages = getValues("languages");
      const gerne = getValues("gerne");
  
      getContainers({
        seconds: duration,
        timeGap: timeGap,
        author: author,
        description: description,
        contributors: contributors,
        country: country,
        place: place,
        source: source,
        languages: languages,
        gerne: gerne,
        title: title,
        
      });
      const videoURL = getValues("videoURL");
      localStorage.setItem("toaVideoURL", JSON.stringify(videoURL));
      setReady(true);
    }
  };

  const onReset = () => {
    // Clear all local storage data
    localStorage.removeItem("toaItemList");
    localStorage.removeItem("toaVideoURL");

    setItems([]);
    setReady(false);
    setCurrentVideoUrl("");
    setShowVideo(false);
    setShowVideoURL("");
    setActiveId(null);
    setCheckURL(false);
    setIsPlaying(false);

    // Reset form values
    setValue("videoURL", "");
    setValue("title", "");
    setValue("timeGapSection", "30");
    setValue("author", "");
    setValue("description", "");
    setValue("contributors", "");
    setValue("country", "");
    setValue("place", "");
    setValue("source", "");
    setValue("languages", "");
    setValue("gerne", "");

  };

  const getPandoraVideo = async (id) => {
    console.log(id)
    const bodyData = {
      action: "find",
      data: { 
        keys: ["title", "id", "editable", "modified", "created", "posterRatio", "director", "year", "featuring", "summary", "duration", "posterFrame"], 
        query: {
          conditions: [{"key": "id", "value": `${JSON.parse(id)}`, "operator": "==" }]
        }
      },
    }
    const result = await fetchPandora(bodyData);
    return result;
  };

  const onExport = async () => {
    const getCurrentData = JSON.parse(localStorage.getItem("toaItemList"));
    console.log(getCurrentData)
    const pandoraId = localStorage.getItem("toaVideoURL");
    const pandoraVideo = await getPandoraVideo(pandoraId);
    console.log(pandoraVideo)

    if(pandoraVideo.data?.items.length > 0) {   
      /* 
      A: Tag
      B: Narration
      C: Data
      D: Categories
      E: References
      F: Event
      G: Place
      */
      let reference_annotations = [];
      let tag_annotations = [];
      let category_annotations = [];
      let event_annotations = [];
      let place_annotations = [];
      let narration_annotations = [];
      let data_annotations = [];
      const getAnnotaitons = [...getCurrentData.children].filter((v) => v.list.length > 0)
      for(let i = 0; i < getAnnotaitons.length; i++) {
        const time = getAnnotaitons[i].time;
        for(let j = 0; j < getAnnotaitons[i].list.length; j++) {
          const result = {
            start: time[0],
            end: time[1],
            type: getAnnotaitons[i].list[j].layer,
            value: {}
          }
          // const result = getAnnotaitons[i].list[j];
          if(result.type === "A") {
            result.type = "tagLayer";
            result.value = getAnnotaitons[i].list[j].input;
            tag_annotations.push(result);
          } else if(result.type === "B") {
            result.type = "narrationLayer";
            result.value = getAnnotaitons[i].list[j].input;
            narration_annotations.push(result);
          } else if(result.type === "C") {
            result.type = "dataLayer";
            result.value = getAnnotaitons[i].list[j].input;
            data_annotations.push(result);
          } else if(result.type === "D") {
            result.type = "categoryLayer";
            result.value = {
              value: CategoryLayerItemData[getAnnotaitons[i].list[j].input.value]
            };
            category_annotations.push(result);
          } else if(result.type === "E") {
            result.type = "referenceLayer";
            result.value = getAnnotaitons[i].list[j].input;
            reference_annotations.push(result);
          } else if(result.type === "F") {
            result.type = "eventLayer";
            result.value = getAnnotaitons[i].list[j].input;
            event_annotations.push(result);
          } else if(result.type === "G") {
            result.type = "placeLayer";
            result.value = getAnnotaitons[i].list[j].input;
            place_annotations.push(result);
          }
        }
      }
      const annotations = {
        reference_annotations: reference_annotations,
        tag_annotations: tag_annotations,
        category_annotations: category_annotations,
        event_annotations: event_annotations,
        place_annotations: place_annotations,
        narration_annotations: narration_annotations,
        data_annotations: data_annotations,
      }

      const videoData = {
        title: getCurrentData.title || pandoraVideo.data?.items[0].title,
        pandora_id: JSON.parse(pandoraId),
        author: getCurrentData.author,
        contributors: Array.isArray(getCurrentData.contributors) ? getCurrentData.contributors.join(", ") : getCurrentData.contributors || (Array.isArray(pandoraVideo.data?.items[0].director) ? pandoraVideo.data?.items[0].director.join(", ") : pandoraVideo.data?.items[0].director),
        description: getCurrentData.description || pandoraVideo.data?.items[0].summary,
        country: getCurrentData.country || pandoraVideo.data?.items[0].country,
        place: getCurrentData.place || pandoraVideo.data?.items[0].place,
        source: getCurrentData.source || pandoraVideo.data?.items[0].source,
        language: getCurrentData.languages || pandoraVideo.data?.items[0].language,
        genre: getCurrentData.gerne || pandoraVideo.data?.items[0].genre,
        start: 0,
        end: pandoraVideo.data?.items[0].duration,
        duration: pandoraVideo.data?.items[0].duration,
        poster: pandoraVideo.data?.items[0].posterRatio,
        annotations: annotations
      }
      console.log(videoData)
      const result = await uploadVideo(videoData).then((res) => {
        // onReset();
        setDone(true);
        console.log(res)
      }).catch((err) => {
        console.log(err)
      });
    }

  };

  const onCreateMore = () => {
    setDone(false);
    onReset();
  
  }

  const urlInputWatch = watch("videoURL");
  useEffect(() => {
    if (urlInputWatch === "" || !Boolean(urlInputWatch)) {
      setAktiv(true);
    } else {
      setAktiv(false);
    }
    setCheckURL(false);
  }, [urlInputWatch]);

  const onShowVideo = ({ seek = false }) => {
    if (!seek) {
      seekTime.current = 0;
    } else {
      seekTime.current = seek;
    }
    if (showVideo) {
      if (timeLineVideoRef.current) {
        // timeLineVideoRef.current.seekTo(seekTime.current, "seconds");
        timeLineVideoRef.current.currentTime = seekTime.current;
        // console.log("move")
      }
    } else {
     
      setShowVideo(true);
      const url = localStorage.getItem("toaVideoURL");
      setShowVideoURL(JSON.parse(url));
      setTimeout(() => {
        if (timeLineVideoRef.current) {
          // timeLineVideoRef.current.seekTo(seekTime.current, "seconds");
          timeLineVideoRef.current.currentTime = seekTime.current;
          // console.log("move")
        }
      },300)
    }
  };

  const onReady = () => {
    if (timeLineVideoRef.current) {
      timeLineVideoRef.current.seekTo(seekTime.current, "seconds");
      setIsPlaying(true);
    }
  };

  const moveTo = () => {
    if (timeLineVideoRef.current && scrollRef.current) {
      const currentTime = Math.floor(timeLineVideoRef.current.currentTime);
      // const currentTime = Math.floor(timeLineVideoRef.current.getCurrentTime());

      //find container
      const containers = items.children;
      const getContainerData = containers.find((val) => {
        if (val.time[0] <= currentTime && val.time[1] > currentTime) {
          return val;
        }
      });
      const cuurrentContainer = document.querySelector(
        `#a${getContainerData.id}`
      );
      cuurrentContainer.style.background = "#FF5C1C";

      scrollRef.current.scrollTo({
        left: cuurrentContainer.offsetLeft,
        behavior: "smooth",
      });
      setTimeout(() => {
        cuurrentContainer.style.background = "rgb(245 245 245)";
      }, [1000]);
    }
  };

  const onLogout = () => {
    logout().then((res) => {
        // onReset();
        window.location.reload()
    })
}
  if (!pandora) {
    return <div>Error</div>;
  }

  return (
    <div
      ref={scrollRef}
      className="w-screen h-screen overflow-x-scroll bg-neutral-300 relative"
    >
      {ready && (
        <Nav
          onReset={onReset}
          onExport={onExport}
          onLogout={onLogout}
          setShowVideo={setShowVideo}
        />
      )}
      {
        (ready && done) && (
          <div className="fixed top-0 left-0 w-full h-full bg-black/50 z-[1000] flex items-center justify-center">
            <div className="bg-white p-8 rounded-lg shadow-lg max-w-md">
              <h2 className="text-2xl font-bold text-center mb-4">Thank you for your data!</h2>
              <p className="text-gray-600 text-center mb-6">Your annotations have been successfully uploaded.</p>
              <div className="flex flex-col gap-4">
                <a 
                  href={process.env.EVA_URL}
                  onClick={() => {
                    onReset();
                  }}
                  target="_blank"
                  className="bg-orange-500 text-white py-2 px-4 rounded hover:bg-orange-600 text-center transition-colors"
                >
                  Visit EVA Website
                </a>
                <a 
                  href={process.env.ADMIN_URL}
                  target="_blank"
                  onClick={() => {
                    onReset();
                  }}
                  className="bg-orange-500 text-white py-2 px-4 rounded hover:bg-orange-600 text-center transition-colors"
                > 
                  Admin Page
                </a>
                <button
                  onClick={onCreateMore}
                  className="border-2 border-orange-500 text-orange-500 py-2 px-4 rounded hover:bg-orange-50 transition-colors"
                >
                  Create More Annotations
                </button>
              </div>
            </div>
          </div>
        )
      }
      {showVideo && ready && (
        <div className="fixed bottom-2 left-2 z-50 bg-white border-2 border-black w-fit max-w-[100vw] rounded-md">
          <div className="w-full flex justify-between items-center border-b-2 border-black">
            <div
              onClick={moveTo}
              className="flex gap-1 items-center px-2 py-1 cursor-pointer font-semibold text-white hover:bg-[#85A6FF] bg-orange-500 text-sm"
            >
              <div>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={2.0}
                  stroke="currentColor"
                  className="size-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M7.5 3.75H6A2.25 2.25 0 0 0 3.75 6v1.5M16.5 3.75H18A2.25 2.25 0 0 1 20.25 6v1.5m0 9V18A2.25 2.25 0 0 1 18 20.25h-1.5m-9 0H6A2.25 2.25 0 0 1 3.75 18v-1.5M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                  />
                </svg>
              </div>
              <div>Jump to &rarr;</div>
            </div>
            <div
              onClick={() => setShowVideo(false)}
              className="px-2 py-1 cursor-pointer font-semibold text-neutral-600 hover:text-orange-500 text-sm"
            >
              Close
            </div>
          </div>
          <div className="flex gap-3 items-center w-full max-w-[900px] max-h-[600px]">
            <div className="flex-[2] flex items-center">
            <video
              ref={timeLineVideoRef}
              src={`${BASE_URL}/${showVideoURL}/480p1.mp4`}
              className="w-full h-full"
              controls={true}
              aria-label="video player"
              preload="auto"
            >
              <source type="video/mp4" />
              Your browser does not support the video tag.
            </video>
            </div>
            {/* <ReactPlayer onReady={onReady} ref={timeLineVideoRef} playing={isPlaying} controls={true} url={showVideoURL} /> */}
            <div className="flex-1 px-2 py-2 max-w-[500px] overflow-y-scroll break-words">
              <div>
                <span className="font-medium">Title</span>: {items.title}
              </div>
              <div>
                <span className="font-medium">Description</span>:{" "}
                {items.description}
              </div>
              <div>
                <span className="font-medium">Contributors</span>:{" "}
                {items.contributors}
              </div>
              <div>
                <span className="font-medium">Place</span>: {items.place}
              </div>
              <div>
                <span className="font-medium">Languages</span>:{" "}
                {items.languages}
              </div>
              <div>
                <span className="font-medium">Genre</span>: {items.gerne}
              </div>
              <div>
                <span className="font-medium">Source</span>: {items.source}
              </div>
              <div>
                <span className="font-medium">Author</span>: {items.author}
              </div>
              <div>
                <span className="font-medium">Country</span>: {items.country}
              </div>  
            </div>
          </div>
        </div>
      )}
      {ready && (
        <div className=" fixed w-fit h-fit bottom-0 left-0 flex px-3 py-2 justify-between items-center z-[100]">
          {!showVideo && (
            <div>
              <div
                onClick={onShowVideo}
                className="driver-d cursor-pointer border-2 border-black bg-white rounded-lg px-2 py-1 hover:bg-black hover:text-white transition-all"
              >
                Full Video
              </div>
            </div>
          )}
        </div>
      )}
      {!ready && (
        <div className="fixed w-screen h-screen bg-white flex flex-col overflow-scroll ">
          <div className="w-full h-[50px] bg-white p-4 flex justify-between items-center">
            <a href={`${process.env.ADMIN_URL}`} target="_blank" className="cursor-pointer hover:text-orange-500">{user.username}</a>
            <div onClick={onLogout} className="cursor-pointer hover:text-orange-500">Logout</div>
          </div>
          <div className="w-full h-full bg-white p-4">
            <div
              style={{ backgroundImage: `url(/logo/logo.png)` }}
              className="flex w-full h-28 bg-contain bg-no-repeat bg-center justify-center mb-8"
            >
            </div>
            <ReactPlayer
              className={`hidden`}
              onReady={onAboutVideo}
              ref={videoRef}
              url={currentVideoUrl}
            />
            <form
              onSubmit={handleSubmit(onUploadVideo)}
              className="flex flex-col"
            >
              <label htmlFor="pandoraVideoList" className="font-medium">
                Pandora Videos
              </label>
              {pandora.length > 0 && (
                <select
                  id="pandoraVideoList"
                  {...register("videoURL")}
                  className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400"
                >
                  {pandora.map((v, idx) => {
                    return (
                      <option value={`${v.id}`} key={idx}>
                        {v.title}
                      </option>
                    );
                  })}
                </select>
              )}
              {checkURL && (
                <div className="text-red-500 text-sm">
                  This URL is incorrect
                </div>
              )}
              <div className="mt-4 flex flex-col gap-2">
                <label htmlFor="timeGapSection" className="font-medium">
                  Time Gaps
                </label>
                <select
                  id="timeGapSection"
                  {...register("timeGapSection")}
                  className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400"
                >
                  <option value={"5"}>5s</option>
                  <option value={"15"}>15s</option>
                  <option value={"30"}>30s</option>
                  <option value={"60"}>60s</option>
                  <option value={"90"}>90s</option>
                  <option value={"120"}>120s</option>
                </select>
              </div>
              <div className="w-full mt-3 flex flex-col driver-g">
                <label className="font-medium">About Video</label>
                <div className="grid grid-cols-2 gap-2">
                <input  
                  {...register("title")}
                  type="text"
                  className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400"
                  placeholder="Title"
                />
                <input
                  {...register("author")}
                  type="text"
                  className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400"
                  placeholder="Author"
                />
                <input
                  {...register("contributors")}
                  type="text"
                  className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400"
                  placeholder="Contributors"
                />
                <input
                  {...register("country")}
                  type="text"
                  className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400"
                  placeholder="Country"
                />
                <input
                  {...register("place")}
                  type="text"
                  className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400"
                  placeholder="Place"
                />
                <input
                  {...register("source")}
                  type="text"
                  className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400"
                  placeholder="Source"
                />
                <input
                  {...register("languages")}
                  type="text"
                  className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400"
                  placeholder="Languages"
                />
                <input
                  {...register("gerne")}
                  type="text"
                  className="border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400"
                  placeholder="Gerne"
                />
                <textarea
                  {...register("description")}
                  className="col-span-2 border border-neutral-400 px-2 py-1 rounded-lg focus:outline-none focus:border-orange-400"
                  placeholder="Description"
                />
                </div>
              
              </div>
              <input
                disabled={false}
                type="submit"
                value="Create Timeline Board"
                className="driver-h mt-8 text-white font-semibold w-full py-2 bg-orange-400 rounded-lg hover:bg-orange-500 cursor-pointer transition-all disabled:bg-gray-400"
              />
            </form>
       
          </div>
        </div>
      )}
      {ready && (
        <div className="w-fit h-[calc(100vh-40px)] p-4 pt-[70px]">
          <DndContext
            id={contextId}
            announcements={defaultAnnouncements}
            sensors={sensors}
            collisionDetection={closestCorners}
            onDragStart={handleDragStart}
            onDragOver={handleDragOver}
            onDragEnd={handleDragEnd}
          >
            <div className="flex gap-4 relative">
              {items.children &&
                items["children"].map((val, idx) => {
                  return (
                    <Container
                      key={val.id}
                      id={val.id}
                      time={val.time}
                      items={val.list}
                      setItems={setItems}
                      onShowVideo={onShowVideo}
                    />
                  );
                })}
              <DragOverlay>
                {activeId ? <Item id={activeId} /> : null}
              </DragOverlay>
            </div>
          </DndContext>
        </div>
      )}
    </div>
  );
};

export default TWrapper;
