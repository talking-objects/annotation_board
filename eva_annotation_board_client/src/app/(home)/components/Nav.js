import { driver } from "driver.js";
import "driver.js/dist/driver.css";
import Image from "next/image";

const Nav = ({ onReset, onExport, setShowVideo, onLogout }) => {
  const driverObj = driver({
    showProgress: true,
    steps: [
      { element: ".driver-a", popover: { title: "Annotation1", description: "Add your Annotations to your selected timeframe." } },
      {
        element: ".driver-b",
        popover: {
          title: "Annotation2",
          description: "You can add different Layers of Annotations",
          onNextClick: () => {
            const btn = document.querySelector(".driver-b");
            btn.click();
            driverObj.moveNext();
          },
        },
      },
      {
        element: ".driver-a",
        popover: {
          title: "Annotation3",
          description: `
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            <div style='display: flex;'><div style='font-weight: bold;'>Personal Tag Layer</div>: Add personal tags to describe key content, themes, and subjects appearing in the video. This helps with content discovery and organization.</div>
            <div style='display: flex;'><div style='font-weight: bold;'>Narration Layer</div>: Add free-form text descriptions, commentary, and narrative details about what is happening in the video. This provides context and interpretation.</div>
            <div style='display: flex;'><div style='font-weight: bold;'>Data Layer</div>: Document factual information, statistics, measurements, dates and other concrete data points referenced in the video content.</div>
            <div style='display: flex;'><div style='font-weight: bold;'>Category Layer</div>: Apply standardized thematic categories defined by the TOA Team to classify and organize video content systematically.</div>
            <div style='display: flex;'><div style='font-weight: bold;'>Reference Layer</div>: Include citations, footnotes, URLs, and connections to related materials that provide additional context and verification.</div>
            <div style='display: flex;'><div style='font-weight: bold;'>Event Layer</div>: Document specific events like births, deaths, ceremonies, meetings, and other time-based occurrences mentioned in the video.</div>
            <div style='display: flex;'><div style='font-weight: bold;'>Place Layer</div>: Record geographic locations such as cities, countries, buildings, and other spatial information referenced in the content.</div>
        </div>
        `,
        },
      },
      { element: ".driver-c", popover: { title: "Annotation4", description: `By clicking this button in the layer section, the video will automatically open and start playing from the time specified in that layer section.` } },
      {
        element: ".driver-d",
        popover: {
          title: "Annotation5",
          description: `<div style="width: 700px; height: 600px;">
          <div>Open the full Video</div>
          <div style='height: 100%; width: 100%; background: url("/logo/01.png"); background-size: contain; background-repeat: no-repeat;' />
          </div>`,
        },
      },
      {
        element: ".driver-d",
        popover: {
            title: "Annotation6",
            description: `<div style="width: 700px; height: 600px;">
            <div>Use the JumpTo Button to jump to the respective Sections of the Timeframe of the Annotation and vice Versa. </div>
            <div style='height: 100%; width: 100%; background: url("/logo/01.png"); background-size: contain; background-repeat: no-repeat;' />
            </div>`,
          },
      },
      {
        element: ".driver-e",
        popover: {
            title: "Export1",
            description: `Once you finish annotating, click the Upload button to save your annotations. Your data will be stored and made available on the EVA website for others to view and use.`,
          },
      },
      {
        
        popover: {
            title: "Good to know",
            description: `Please note, that your Annotations are not stored/saved. Once you close your Browser or click the Reset Button, your Data will be Lost.`,
          },
      },
    ],
  });
  const openExplanation = () => {
    setShowVideo(false)
    driverObj.drive();
  };
  return (
    <div className="h-[60px] w-screen bg-white fixed top-0 left-0 flex justify-between items-center px-4">
      <div className="flex gap-8 items-center">
        <a href={`${process.env.ADMIN_URL}`} target="_blank" style={{backgroundImage: `url(/logo/logo.png)`}}  className="w-32 h-24 bg-contain bg-no-repeat bg-center">
         
        </a>
        <div onClick={openExplanation} className="cursor-pointer bg-white rounded-lg px-2 py-1 hover:bg-black hover:text-white transition-all">
          How to use?
        </div>
      </div>
      <div className="flex gap-3">
        <div onClick={onLogout} className="cursor-pointer bg-white rounded-lg px-2 py-1 hover:bg-black hover:text-white transition-all">
          Logout
        </div>
        <div onClick={onReset} className="cursor-pointer bg-white rounded-lg px-2 py-1 hover:bg-black hover:text-white transition-all">
          Reset
        </div>
        <div onClick={onExport} className="driver-e cursor-pointer bg-white rounded-lg px-2 py-1 hover:bg-black hover:text-white transition-all">
          Upload
        </div>
      </div>
    </div>
  );
};

export default Nav;
