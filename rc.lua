local awful = require("awful")
local awful_rules = require("awful.rules")
local beautiful = require("beautiful")
local naughty = require("naughty")

-- {{{ Error handling
-- Check if awesome encountered an error during startup and fell back to
-- another config (This code will only ever execute for the fallback config)
if awesome.startup_errors then
    naughty.notify({ preset = naughty.config.presets.critical,
                     title = "Oops, there were errors during startup!",
                     text = awesome.startup_errors })
end

-- Handle runtime errors after startup
do
    local in_error = false
    awesome.connect_signal("debug::error", function (err)
        -- Make sure we don't go into an endless error loop
        if in_error then return end
        in_error = true

        naughty.notify({ preset = naughty.config.presets.critical,
                         title = "Oops, an error happened!",
                         text = tostring(err) })
        in_error = false
    end)
end
-- }}}


onboard = {}
home_screen = {}

focus_next_client = function ()
  if awful.client.next(1) == home_screen.client then
    awful.client.focus.byidx( 2 )
  else
    awful.client.focus.byidx( 1 )
  end

  if client.focus then
    client.focus:raise()
  end
end

focus_client_by_window_id = function (window_id)
  for _, c in ipairs(client.get()) do
    if c.window == window_id then
      client.focus = c
      if client.focus then
        client.focus:raise()
      end
    end
  end
end

launch_home_screen = function ()
  if home_screen.client then
    client:kill()
    home_screen = {}
  end
  awful.spawn.with_shell("/home/chip/pocketchip-menu/load.sh", {name="Menu", fullscreen=true, type="desktop"})
end

focus_home_screen = function ()
  if home_screen.client then
    client.focus = home_screen.client
    if client.focus then
      client.focus:raise()
    end
  else
    launch_home_screen()
  end
end
hide_mouse_cursor = function ()
  awful.util.spawn_with_shell("xsetroot -cursor $HOME/.config/awesome/blank_ptr.xbm $HOME/.config/awesome/blank_ptr.xbm")
end

modkey = "Mod1"
awful.layout.layouts = {
    awful.layout.suit.max.fullscreen
}

tags = {}
for s = 1, screen.count() do
  tags[s] = awful.tag({ 1 }, s, awful.layout.layouts[1])
end

root.buttons(awful.util.table.join(
  awful.button({ }, 4, awful.tag.viewnext),
  awful.button({ }, 5, awful.tag.viewprev)
))
local all_minimized = false
function toggle_minimize_all()
  all_minimized = not all_minimized

  for _, c in ipairs(mouse.screen.selected_tag:clients()) do
    naughty.notify({text=c.name})
    if not (c.name == "Menu") then  
      c.minimized = all_minimized
    end
  end
end

local globalkeys = awful.util.table.join(
  awful.key({ }                  , "XF86PowerOff", toggle_minimize_all),
  awful.key({ modkey,           }, "Tab", focus_next_client),
  awful.key({ "Control",        }, "Tab", focus_next_client),
  awful.key({ modkey,           }, "Return", function () awful.util.spawn("dmenu_run", false) end)
)

local clientkeys = awful.util.table.join(
  awful.key({ "Control"         }, "q",
    function (c)
      if c ~= home_screen.client then
        c:kill()
      end
    end)
)
local keynumber = 0
for s = 1, screen.count() do
  keynumber = math.min(9, math.max(#tags[s], keynumber));
end

local clientbuttons = awful.util.table.join(
  awful.button({ }, 1, function (c) client.focus = c; c:raise() end),
  awful.button({ modkey }, 1, awful.mouse.client.move),
  awful.button({ "Control" }, 1, function (c) awful.util.spawn("xdotool click 3", false) end))

root.keys(globalkeys)

awful_rules.rules = {
 { rule = { },
    properties = { border_width = 0,
      border_color = beautiful.border_normal,
      focus = true,
      keys = clientkeys,
      buttons = clientbuttons } }
}

client.add_signal("manage", function (c, startup)
  if c.name == "Menu" then
    home_screen.client = c
  elseif c.class == "ahoy" then
    onboard.client = c
    c.ontop = true
  end

  if not startup then
    if not c.size_hints.user_position and not c.size_hints.program_position then
      awful.placement.no_overlap(c)
      awful.placement.no_offscreen(c)
    end
  end
end)
client.add_signal("unmanage", function (c)
  if c.name == "Menu" then
    home_screen = {}
  elseif c.class == "ahoy" then
    onboard = {}
  end
end)



-- hide_mouse_cursor()
launch_home_screen()