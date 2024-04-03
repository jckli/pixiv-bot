package main

import (
	"context"
	"fmt"
	"github.com/disgoorg/disgo/bot"
	"github.com/jckli/picsiv/src/commands"
	"github.com/jckli/picsiv/src/dbot"
	_ "github.com/joho/godotenv/autoload"
	"os"
	"os/signal"
	"syscall"
	"time"
)

func main() {
	picsiv := dbot.New(os.Getenv("VERSION"))

	h := commands.CommandHandlers(picsiv)

	client := picsiv.Setup(
		h,
		bot.NewListenerFunc(picsiv.ReadyEvent),
	)

	var err error
	if picsiv.Config.DevMode {
		picsiv.Logger.Info(
			fmt.Sprintf(
				"Running in dev mode. Syncing commands to server ID: %s",
				picsiv.Config.DevServerID,
			),
		)
		_, err = client.Rest().
			SetGuildCommands(client.ApplicationID(), picsiv.Config.DevServerID, commands.CommandList)
	} else {
		picsiv.Logger.Info(
			"Running in global mode. Syncing commands globally.",
		)
		_, err = client.Rest().SetGlobalCommands(client.ApplicationID(), commands.CommandList)
	}
	if err != nil {
		picsiv.Logger.Error(fmt.Sprintf("Failed to sync commands: %s", err.Error()))
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	err = client.OpenGateway(ctx)
	if err != nil {
		picsiv.Logger.Error("Error while connecting: ", err)
	}
	defer client.Close(context.TODO())

	picsiv.Logger.Info("Bot is now running.")
	s := make(chan os.Signal, 1)
	signal.Notify(s, syscall.SIGINT, syscall.SIGTERM, os.Interrupt)
	<-s
	picsiv.Logger.Info("Shutting down...")
}
