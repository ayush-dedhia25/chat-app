import StatusListHeader from "./StatusListHeader";
import StatusListItem from "./StatusListItem";

function StatusList() {
  return (
    <div className="flex flex-col w-[25%] bg-neutral-900">
      <StatusListHeader />

      <div className="flex-1 my-4 overflow-y-auto no-scrollbar">
        <h3 className="mx-4 mb-2 text-sm text-zinc-400">Recent updates</h3>
        <div className="px-3">
          <StatusListItem
            name="Ayush Dedhia"
            timestamp="Today, 21:32"
            profile="https://usatodayhss.com/wp-content/uploads/sites/96/2022/08/11268798.jpeg?w=1000&h=600&crop=1"
          />
          <StatusListItem
            name="John Doe"
            timestamp="Today, 04:02"
            profile="https://usatodayhss.com/wp-content/uploads/sites/96/2022/08/11268798.jpeg?w=1000&h=600&crop=1"
          />
        </div>
      </div>
    </div>
  );
}

export default StatusList;
