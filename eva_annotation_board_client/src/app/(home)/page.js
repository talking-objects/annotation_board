
import { fetchPandora } from "../utils/hooks/fetchPandora";
import HomeWrapper from "./components/HomeWrapper";

const getVideoList = async () => {
    const bodyData = {
      action: "find",
      data: { keys: ["title", "id", "editable", "modified", "created", "posterRatio", "director", "year", "featuring", "summary", "duration", "posterFrame"], query: { conditions: [], operator: "&" }, sort: [{ key: "title", operator: "-" }] },
    }
    const result = await fetchPandora(bodyData);
    return result;
  };

const TimeLinePage2 = async () => {
    const data = await getVideoList()
    

    return (
      <HomeWrapper pandora={data} /> 
    )
}

export default TimeLinePage2;