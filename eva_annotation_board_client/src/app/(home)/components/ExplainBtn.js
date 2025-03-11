import { driver } from "driver.js";
import "driver.js/dist/driver.css";

const ExplainBtn = () => {
    const driverObj = driver({
        showProgress: true,
        steps: [
          { element: '.driver-f', popover: { title: 'Create1', description: 'Copy and paste the Link from Youtube into the »Write video Url« Field' } },
          { element: '.driver-g', popover: { title: 'Create2', description: 'Optionally add further Informations (Creator, Textdescription, Contributors, etc.)' } },
          { element: '.driver-h', popover: { title: 'Create3', description: 'Once you are finish click on »Create Timeline Board«' } },
          
        ]
      });
  const openExplanation = () => {
    driverObj.drive()
  }
    return (
        <div onClick={openExplanation} className="flex justify-end text-sm mt-2 font-medium text-neutral-500 cursor-pointer hover:text-orange-500">How to use?</div>
    )
}

export default ExplainBtn;