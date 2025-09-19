import { useEffect, useState } from "react";
import { Avatar, Card, CardHeader, CardBody } from "@heroui/react";
import { TabNavigation } from "@/components/TabNavigation";
import {
  PencilSimpleLineIcon,
  UserIcon,
  TelegramLogoIcon,
  CloverIcon,
} from "@phosphor-icons/react";
import useAuth from "@/hooks/useAuth";

export default function Profile() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen mx-4">
      <div className="flex flex-col items-center pt-10 gap-6">
        {/* Header */}
        <div>
          <span className="font-bold text-large">Profile</span>
        </div>
        <div className="relative">
          {user?.photo_url ? (
            <img
              src={user?.photo_url}
              alt={user?.firstName}
              className={`w-32 h-32 object-cover rounded-full border-5  ${
                location.pathname == "/profile"
                  ? "border-primary"
                  : "border-gray-300"
              }`}
            />
          ) : (
            <Avatar className="w-32 h-32 border-5 text-gray-500" />
          )}

          <button className="cursor-pointer absolute bg-primary flex p-2 rounded -bottom-2 -right-2">
            <PencilSimpleLineIcon size={25} className="text-white" />
          </button>
        </div>

        {/* Personal info */}

        <div className="max-w-sm min-w-3xs w-full mx-auto p-4 sm:p-6 bg-white rounded-md shadow-md/8">
          <Card className="flex flex-col gap-4 rounded-t-none">
            <CardHeader className="flex justify-between items-center p-0">
              <p className="font-semibold text-md">Personal info</p>
              <button className="rounded-md cursor-pointer px-2 py-1 font-semibold text-sm text-white bg-primary">
                Edit
              </button>
            </CardHeader>
            <CardBody className="flex flex-col p-0 gap-2">
              <div className="flex justify-start gap-4 items-center">
                <UserIcon size={24} />
                <div className="flex flex-col">
                  <span className="text-sm text-gray-400">Name</span>
                  <p className="text-md">
                    {user?.lastName
                      ? `${user.firstName} ${user.lastName}`
                      : user?.firstName || "Гость"}
                  </p>
                </div>
              </div>
              <div className="flex justify-start gap-4 items-center">
                <TelegramLogoIcon size={24} />
                <div className="flex flex-col">
                  <span className="text-sm text-gray-400">Username</span>
                  <p className="text-md">
                    {user?.userName ? `@${user?.userName}` : "@Гость"}
                  </p>
                </div>
              </div>
              <div className="flex justify-start gap-4 items-center">
                <CloverIcon size={24} />
                <div className="flex flex-col">
                  <span className="text-sm text-gray-400">Premium</span>
                  <p className="text-md">{user?.is_premium ? "Yes" : "No"}</p>
                </div>
              </div>
            </CardBody>
          </Card>
        </div>
        <TabNavigation />
      </div>
    </div>
  );
}
