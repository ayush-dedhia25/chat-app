import CallListHeader from "./CallListHeader";
import CallListItem from "./CallListItem";

function CallList() {
  return (
    <div className="flex flex-col w-[25%] bg-neutral-900">
      <CallListHeader />

      <h3 className="mx-4 mt-5 mb-2 text-sm text-zinc-400">Recent calls</h3>

      <div className="flex-1 px-3 mb-4 space-y-1 overflow-y-auto no-scrollbar">
        <CallListItem
          name="Ayush"
          timestamp="21:32"
          callType="missed"
          profile="https://usatodayhss.com/wp-content/uploads/sites/96/2022/08/11268798.jpeg?w=1000&h=600&crop=1"
        />
        <CallListItem
          name="Ayush"
          timestamp="06-03-2024"
          callType="outgoing"
          profile="https://usatodayhss.com/wp-content/uploads/sites/96/2022/08/11268798.jpeg?w=1000&h=600&crop=1"
        />
      </div>
    </div>
  );
}

export default CallList;
