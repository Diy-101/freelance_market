import { useState } from "react";
import {
  Badge,
  Avatar,
  Card,
  CardHeader,
  CardBody,
  ButtonGroup,
  Button,
} from "@heroui/react";
import { TabNavigation } from "@/components/TabNavigation";
import {
  PencilSimpleLineIcon,
  UserIcon,
  TelegramLogoIcon,
  AddressBookIcon,
  CloverIcon,
} from "@phosphor-icons/react";

export default function Profile() {
  const [roleTab, setRoleTab] = useState(false);

  const onClickWorker = () => {
    setRoleTab(false);
  };
  const onClickSeller = () => {
    setRoleTab(true);
  };

  return (
    <div className="flex flex-col items-center min-h-screen w-screen pt-10 gap-6">
      {/* Header */}
      <div>
        <span className="font-bold text-2xl">Profile</span>
      </div>
      <div className="relative">
        <Badge
          isOneChar
          showOutline={false}
          className="absolute bg-primary flex place-content-center h-12 w-12 rounded -bottom-8 -right-3"
          placement="top-right"
          content={<PencilSimpleLineIcon size={25} className="text-white" />}
        >
          <Avatar className="w-36 h-36 border-5" />
        </Badge>
      </div>

      {/* Personal info */}
      <div className="w-sm bg-white rounded-xl shadow-md/8">
        <Card className="flex flex-col p-5 gap-6">
          <CardHeader className="flex justify-between items-end p-0">
            <p className="font-semibold text-2xl">Personal info</p>
            <span className="font-bold text-md">Edit</span>
          </CardHeader>
          <CardBody className="flex flex-col p-0 gap-2">
            <div className="flex justify-start gap-4 items-center">
              <UserIcon size={28} />
              <div className="flex flex-col">
                <span className="text-md text-gray-400">Name</span>
                <p className="text-xl">Ivan Romanov</p>
              </div>
            </div>
            <div className="flex justify-start gap-4 items-center">
              <TelegramLogoIcon size={28} />
              <div className="flex flex-col">
                <span className="text-md text-gray-400">Username</span>
                <p className="text-xl">@username</p>
              </div>
            </div>
            <div className="flex justify-start gap-4 items-center">
              <CloverIcon size={28} />
              <div className="flex flex-col">
                <span className="text-md text-gray-400">Premium</span>
                <p className="text-xl">Yes</p>
              </div>
            </div>
          </CardBody>
        </Card>
      </div>

      {/* Worker and seller profiles */}
      <ButtonGroup className="w-sm justify-evenly bg-white rounded-xl text-xl shadow-md/8">
        <Button
          onPress={onClickWorker}
          className={`flex-1 m-2 rounded-xl font-medium ${
            roleTab == false ? "bg-primary text-white" : ""
          }`}
        >
          Worker
        </Button>
        <Button
          onPress={onClickSeller}
          className={`flex-1 m-2 rounded-xl font-medium ${
            roleTab ? "bg-primary text-white" : ""
          }`}
        >
          Seller
        </Button>
      </ButtonGroup>

      <TabNavigation />
    </div>
  );
}
